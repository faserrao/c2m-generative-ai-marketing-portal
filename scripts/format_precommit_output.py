#!/usr/bin/env python3

import subprocess
import re
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def run_precommit():
    try:
        # Run the pre-commit command and capture the output
        result = subprocess.run(
            ['pre-commit', 'run', '--all-files'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        print(Fore.RED + "Error: pre-commit is not installed or not found in PATH.")
        sys.exit(1)

def parse_output(output):
    """
    Parses the pre-commit output and formats it.
    """
    formatted_output = []
    hook_pattern = re.compile(r'^\s*\S+?:\s+(Passed|Failed|Skipped)')

    for line in output.splitlines():
        match = hook_pattern.match(line)
        if match:
            status = match.group(1)
            if status == "Passed":
                line = Fore.GREEN + line + Style.RESET_ALL
            elif status == "Failed":
                line = Fore.RED + line + Style.RESET_ALL
            elif status == "Skipped":
                line = Fore.YELLOW + line + Style.RESET_ALL
        formatted_output.append(line)
    
    return "\n".join(formatted_output)

def summarize_output(output):
    """
    Provides a summary of the pre-commit run.
    """
    passed = len(re.findall(r'Passed', output))
    failed = len(re.findall(r'Failed', output))
    skipped = len(re.findall(r'Skipped', output))
    
    summary = (
        f"\nSummary:\n"
        f"{Fore.GREEN}Passed:{Style.RESET_ALL} {passed} hooks\n"
        f"{Fore.RED}Failed:{Style.RESET_ALL} {failed} hooks\n"
        f"{Fore.YELLOW}Skipped:{Style.RESET_ALL} {skipped} hooks\n"
    )
    return summary

def main():
    stdout, stderr, returncode = run_precommit()
    
    if stderr:
        print(Fore.RED + "Error Output:\n" + stderr + Style.RESET_ALL)
    
    formatted_stdout = parse_output(stdout)
    print(formatted_stdout)
    
    summary = summarize_output(stdout)
    print(summary)
    
    sys.exit(returncode)

if __name__ == "__main__":
    main()

