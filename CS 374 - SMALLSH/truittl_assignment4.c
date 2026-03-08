#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <errno.h>

#define INPUT_LENGTH 2048
#define MAX_ARGS		 512

bool foreground_mode = false;
bool pending_sigtstp = false;
bool prev_process_terminated = false;
pid_t group_leader = -1;
pid_t current_process_pid = -1;

struct command_line
{
	char *argv[MAX_ARGS + 1];
	int argc;
	char *input_file;
	char *output_file;
	bool is_bg;
};

struct command_line *parse_input()
{
	char input[INPUT_LENGTH];
	struct command_line *curr_command = (struct command_line *) calloc(1, sizeof(struct command_line));

	// Get input
	printf(": ");
	fflush(stdout);
	fgets(input, INPUT_LENGTH, stdin);

	// Tokenize the input
	char *token = strtok(input, " \n");
	while(token){
		if(!strcmp(token,"<")){
			curr_command->input_file = strdup(strtok(NULL," \n"));
		} else if(!strcmp(token,">")){
			curr_command->output_file = strdup(strtok(NULL," \n"));
		} else if(!strcmp(token,"&")){
			curr_command->is_bg = true;
		} else{
			curr_command->argv[curr_command->argc++] = strdup(token);
		}
		token=strtok(NULL," \n");
	}
	return curr_command;
}

int executeBuiltInCommands(struct command_line* command, int status);

int executeOtherCommands(struct command_line* command, int* status);

void echoInput(struct command_line* command_input);

void handle_sigtstp(int signal);

int main()
{
  // Signal Handling for sigtstp for parent
  struct sigaction handler2 = {0};
  handler2.sa_handler = &handle_sigtstp;
  sigemptyset(&handler2.sa_mask);
  handler2.sa_flags = SA_RESTART;
  sigaction(SIGTSTP, &handler2, NULL);

  // By default, ctrl-c should be ignored by parent process
  struct sigaction ignore_ctrl_c = {0};
  ignore_ctrl_c.sa_handler = SIG_IGN;
  sigemptyset(&ignore_ctrl_c.sa_mask);
  ignore_ctrl_c.sa_flags = 0;
  sigaction(SIGINT, &ignore_ctrl_c, NULL);

  // Variables
	struct command_line *curr_command;
  int status = 0;

  setpgid(0,0);
  group_leader = getpid();

	while(true)
	{
    // Collect any finished background processes
    int status_background;
    pid_t pid;
    pid = waitpid(-1, &status_background, WNOHANG);
    while (pid > 0) {
      if(WIFEXITED(status_background)) {
        printf("background pid %d is done: exit value %d\n", pid, WEXITSTATUS(status_background));
      }
      // Child was terminated
      if(WIFSIGNALED(status_background)) {
        printf("background pid %d is done: terminated by signal %d\n", pid, status_background);
      }
      pid = waitpid(-1, &status_background, WNOHANG);
    }

    // Get User Input
		curr_command = parse_input();

    // Check if input is a blank line
    if(curr_command->argc == 0) {
      continue;
    }

    // Check if input is a comment
    if(curr_command->argv[0] != NULL) {
      char first_letter = curr_command->argv[0][0];
      if(strcmp(&first_letter, "#") == 0) {
        continue;
      }
    }

    // Check if input is a built-in command
    // If output == 0, then the command was an inbuilt command and was executed
    // If output == 1, pass this command to another function
    int output = executeBuiltInCommands(curr_command, status);

    // If the command excuted was built-in, we're done
    if(output == 0) {
      continue;
    }

    // Else, run the command with exec
    executeOtherCommands(curr_command, &status);
	}
  // Return is handled via executeBuiltInCommands when the user enters 'exit'
}

int executeBuiltInCommands(struct command_line* command, int status) {
  // exit
  if(strcmp(command->argv[0], "exit") == 0) {
    // Parent should ignore sigterm, so it doesn't terminate itself
    struct sigaction ignore_sigterm = {0};
    ignore_sigterm.sa_handler = SIG_IGN;
    sigemptyset(&ignore_sigterm.sa_mask);
    ignore_sigterm.sa_flags = 0;
    sigaction(SIGTERM, &ignore_sigterm, NULL);

    // Send SIGTERM to every group member (all child processes)
    kill(-group_leader, SIGTERM);
    
    // Exit
    exit(EXIT_SUCCESS);
  }

  // status
  else if(strcmp(command->argv[0], "status") == 0) {
    // If the last foreground process was terminated
    if(prev_process_terminated) {
      printf("terminated by signal %d\n", status); fflush(stdout);
    }
    // If the last foreground process exited
    else {
      printf("exit value %d\n", status); fflush(stdout);
    }  
    return 0;
  }

  // cd
  else if(strcmp(command->argv[0], "cd") == 0) {
    if(command->argv[1] == NULL) {
      char *home_dir = getenv("HOME");
      chdir(home_dir);
    }
    else {
      chdir(command->argv[1]);
    }
    return 0;
  }
  return 1;
}

int executeOtherCommands(struct command_line* command, int* status) {  
  // Fork Program
  current_process_pid = fork();
  if(current_process_pid == -1) {
    printf("Error Forking Process\n"); fflush(stdout);
    return 1;
  }

  // Child
  if(current_process_pid == 0) {
    setpgid(0, group_leader);

    // All Children must ignore SIGTSTP
    struct sigaction mask_sigtstp = {0};
    mask_sigtstp.sa_handler = SIG_IGN;
    sigemptyset(&mask_sigtstp.sa_mask);
    mask_sigtstp.sa_flags = 0;
    sigaction(SIGTSTP, &mask_sigtstp, NULL);

    // If child is run in foreground, reenable sigint handler
    if(foreground_mode == true || command->is_bg == false) {     
      struct sigaction enable_ctrl_c = {0};
      enable_ctrl_c.sa_handler = SIG_DFL;
      sigemptyset(&enable_ctrl_c.sa_mask);
      enable_ctrl_c.sa_flags = 0;
      sigaction(SIGINT, &enable_ctrl_c, NULL);
    }

    // Handle Input
    if(command->input_file != NULL) {
      int in_file = open(command->input_file, O_RDONLY);
      if(in_file == -1){
        printf("cannot open %s for input\n", command->input_file); fflush(stdout);
        *status = 1;
        exit(EXIT_FAILURE);
      }
      dup2(in_file, STDIN_FILENO);
      close(in_file);
    }
    // Handle Output
    if(command->output_file != NULL) {
      int out_file = open(command->output_file, O_WRONLY | O_TRUNC | O_CREAT, 0777);
      if(out_file == -1){
        printf("%s: no such file or directory\n", command->output_file); fflush(stdout);
        *status = 1;
        exit(EXIT_FAILURE);
      }
      dup2(out_file, STDOUT_FILENO);
      close(out_file);
    }

    // If child is run in background redirect input output to /dev/null if user didn't specify
    if(foreground_mode == false && command->is_bg == true) {     
      if(command->input_file == NULL) {
        int in_null = open("/dev/null", O_RDONLY);
        if(in_null == -1) {
          printf("cannot open /dev/null for output\n"); fflush(stdout);
          *status = 1;
          exit(EXIT_FAILURE);
        }
        dup2(in_null, STDIN_FILENO);
        close(in_null);
      }
      if(command->output_file == NULL) {
        int out_null = open("/dev/null", O_WRONLY | O_TRUNC | O_CREAT, 0777);
        if(out_null == -1) {
          printf("cannot open /dev/null for output\n"); fflush(stdout);
          *status = 1;
          exit(EXIT_FAILURE);
        }
        dup2(out_null, STDOUT_FILENO);
        close(out_null);
      }
    }

    // Execute function
    execvp(command->argv[0], command->argv);

    // If the errno from exec failing is two, print that no such file exists.
    if(errno == 2) {
      printf("%s: no such file or directory\n", command->argv[0]);
    }
    // Exit in case of failure
    exit(EXIT_FAILURE);
  }
  // Parent
  else {
    // Run in foreground (wait)
    if(foreground_mode == true || command->is_bg == false) {
      int childStatus;
      waitpid(current_process_pid, &childStatus, 0);
      // Child exited correctly (Doesn't mean the command was correct)
      if(WIFEXITED(childStatus)) {
        int childCode = WEXITSTATUS(childStatus);
        if(childCode != 0) {
          *status = 1;
        }
        else {
          *status = 0;
        }
        prev_process_terminated = false;
      }
      // Child was terminated
      if(WIFSIGNALED(childStatus)) {
        printf("terminated by signal %d\n", WTERMSIG(childStatus)); fflush(stdout);
        prev_process_terminated = true;
        *status = WTERMSIG(childStatus);
      }
    }
    // Run in background (don't wait)
    else {
      printf("background pid is %d\n", current_process_pid); fflush(stdout);
    } 
  }
  current_process_pid = -1;
  if(pending_sigtstp) {
    pending_sigtstp = false;
    if(foreground_mode) {
      // entered
      printf("\nEntering foreground-only mode (& is now ignored)\n"); fflush(stdout);
    }
    else {
      // exited
      printf("\nExiting foreground-only mode\n"); fflush(stdout);
    }
  }
  return 0;
}

void handle_sigtstp(int signal) {
  // When current_process_pid is not -1, it means something is running in the foreground
  if(current_process_pid != -1) {
    pending_sigtstp = true;
    foreground_mode = !foreground_mode;
    return;
  }

  char* message1 = "\nEntering foreground-only mode (& is now ignored)\n: ";
  char* message2 = "\nExiting foreground-only mode\n: ";
  if(foreground_mode) {
    //exit
    write(STDOUT_FILENO, message2, strlen(message2));
  }
  else {
    //enter
    write(STDOUT_FILENO, message1, strlen(message1));
  }
  foreground_mode = !foreground_mode;
  return;
}