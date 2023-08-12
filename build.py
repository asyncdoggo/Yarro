import glob
import shutil
import os
import subprocess


files = ["app", "run.py", "build.py", "requirements.txt", ".gitignore", "LICENSE", "README.md"]
print("Copying files...")


if os.path.exists("./app/record.log"):
    os.remove("./app/record.log")

for i in files:
    if not os.path.isfile(i):
        shutil.copytree(i, f"./build_files/{i}")
    else:
        shutil.copy(i, f"./build_files/{i}")


with open("./build_files/app/static/css/input.css", "w") as file:
    file.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

with open("./build_files/tailwind.config.js", "w") as file:
    file.write("""
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
""")

print("Building tailwind css files")
cmd = "npx tailwindcss -i ./build_files/app/static/css/input.css -o ./build_files/app/static/css/output.css -c " \
      "./build_files/tailwind.config.js"

subprocess.run(cmd, shell=True, check=True)

files = glob.glob("./build_files/app/templates/**/*.html",recursive=True)

for i in files:
    with open(i) as file:
        x = file.read()
    with open(i, "w") as file:
        x = x.replace("""<script src="https://cdn.tailwindcss.com"></script>""",
                      """<link rel="stylesheet" href="/static/css/output.css">""")
        file.write(x)

os.remove("./build_files/app/static/css/input.css")
os.remove("./build_files/tailwind.config.js")

print("build done")

# gh-pages -d .\build_files\ -b build
