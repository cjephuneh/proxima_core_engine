filename = "newrequirements.txt"

# Read the file content
with open(filename, "r") as file:
    lines = file.readlines()

# Remove the content after "==" sign from each line
updated_lines = [line.split(">=")[0] for line in lines]

# Save the updated content back to the file
with open(filename, "w") as file:
    file.writelines(updated_lines)

print("Content removed successfully.")
