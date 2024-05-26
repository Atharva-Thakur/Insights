import subprocess
def run_script():
        try:
            # Run the script
            result = subprocess.run(
                ['python', 'code.py'],
                capture_output=True,  # Capture stdout and stderr
                text=True             # Get the output as string
            )

            # Check the return code to determine if an error occurred
            if result.returncode != 0:
                print("Script failed with error:")
                print(result.stderr)
                return 1,result.stderr
            else:
                print("Script completed successfully:")
                print(result.stdout)
                return 0,result.stdout
        except Exception as e:
            print(f"Failed to run the script: {e}")
            return 2,e