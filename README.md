# Static Site Generator
## Description
A python script to convert markdown files into html files. This project is one of the guided projects in [boot.dev](https://www.boot.dev/courses/build-static-site-generator-python)

## How to Use This Project
Run shell below to download the project:
```bash
git clone https://github.com/zulkou/static-site-generator.git
cd static-site-generator
```
Put your own customized `.md` files at `content/`, `.css` file at `static/` and images at `static/images/`. And if all set, run this:
```bash
./main.sh
```
After running the script, your static site should be automatically hosted at `http://localhost:8888/`, or if you want to disable the hosting, you can delete this line from `main.sh`:
```shell
cd public && python3 -m http.server 8888
```
