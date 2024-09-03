# owl
###### a high priority FalcoLabs project
[![GH Actions](https://img.shields.io/badge/CI-GitHub_Actions-blue?logo=github-actions&logoColor=white)](https://github.com/falcolabs/owl/actions "Go to GitHub Actions page") [![linter](https://github.com/falcolabs/owl/actions/workflows/ohiodetector.yml/badge.svg)](https://github.com/falcolabs/owl/actions/workflows/ohiodetector.yml "Go to Linter page") [![ms windows build](https://github.com/falcolabs/owl/actions/workflows/michaelsoft.yml/badge.svg)](https://github.com/falcolabs/owl/actions/workflows/michaelsoft.yml "Go to Windows build page") [![linux build](https://github.com/falcolabs/owl/actions/workflows/leenux.yml/badge.svg)](https://github.com/falcolabs/owl/actions/workflows/leenux.yml "Go to Linux build page")
<br />
[![Made with Python](https://img.shields.io/badge/Python->=3.12-blue?logo=python&logoColor=white)](https://python.org "Go to Python homepage") [![Made with Node.js](https://img.shields.io/badge/Node.js->=22-blue?logo=node.js&logoColor=white)](https://nodejs.org "Go to Node.js homepage") [![Made with TypeScript](https://img.shields.io/badge/TypeScript-4-blue?logo=typescript&logoColor=white)](https://typescriptlang.org "Go to TypeScript homepage") [![Made with Rust](https://img.shields.io/badge/Rust-2021-blue?logo=rust&logoColor=white)](https://www.rust-lang.org/ "Go to Rust homepage")
<br />
![meme1](https://forthebadge.com/images/featured/featured-powered-by-electricity.svg)

Open source development for a high performance Rust communication engine, primarily for game show use.

## Technical overview
The server software will host a web service and a WebSockets server on a
hard-coded IP adress and port at `localhost:6942/`.

The Python bindings is manually typed and wheel built using PyO3.
The JavaScript bindings is automatically generated using wasm-

The protocol in which the client and server communicates in is based
on `serde` serialization of Rust structs. Bindings for Python and
JavaScript is available (see `engine/engine.pyi` and the generated
`node_modules/client/client.d.ts`)

## Hacking
* Install Rust using rustup and use cargo to run the server.
* Install a JavaScript runtime, either Bun or Node.
* Install a Python implementation, preferably PyPy or CPython.
  Install maturin, a Python library which automatically
  generates Python bindings.

You may find project files from various subprojects in these
directories:
| Subproject             | Directory                  |
|------------------------|----------------------------|
| User Interface         | `/frontend/src/`             |
| Server Logic           | `/server/logic/`             |
| Server Utilities       | `/server/penguin/`           |
| Engine & APIs          | `/engine/src/`               |
| Engine Bindings Python | `/engine/engine.pyi`         |
| Client Communications  | `/frontend/client/src/`      |
| Client Bindings TS     | `/frontend/client/src/types` |

Building
--------
See Hacking (above) for requirements. After that, the project may be built. Note that the Python bindings is automatically built by Actions and can be found [here](https://github.com/falcolabs/owl/actions) (`Michaelsoft Binbows` for Windows, `Penguin` for Linux),
### For `gang`
  * For client, use `gang front`. The Rust module will be automatically
    compiled and bundled, and hot-reload enabled Vite starts serving on
    localhost:5173/.
  * For server, use `gang run`. The Rust module will be compiled,
    the Python binding generated, the wheel built and installed automatically.
    `server/main.py` is subsequenly called, with `server/` as current directory.

### Non-`gang`
  * For client, use any JavaScript runtime to invoke `compileRustDev` in `package.json`, like `bun run dev`, `npm run dev`, `yarn dev`, etc.
  * For server, compile the Python bindings with `maturin develop` (or if you want a `.whl` file, use `maturin build -o <name>`). Change your directory into `server/`, and run `main.py`.

Licensing & Copyright
---------------------
```
Copyright (c) 2023-2024 FalcoLabs.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
