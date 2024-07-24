OWL
- a high priority Team Falco project 
======================
Open source development of the new Rust engine

Technical specifications
------------------------
The server software will host a web service and a WebSockets server on a 
hard-coded IP adress and port at `localhost:6942/`.

The Python bindings is manually typed and wheel built using PyO3.
The JavaScript bindings is automatically generated using wasm-

The protocol in which the client and server communicates in is based
on `serde` serialization of Rust structs. Bindings for Python and 
JavaScript is available (see `engine/engine.pyi` and the generated
`node_modules/client/client.d.ts`)

Development
-----------
* Install Rust using rustup and use cargo to run the server.
* Install a JavaScript runtime, either Bun or Node.
* Install a Python implementation, preferably PyPy or CPython.
  Install maturin, a Python library which automatically
  generates Python bindings.

You may find project files from various subprojects in these
directories:
|------------------------+-----------------------|
| SUBPROJECT             | DIRECTORY             |
|========================+=======================|
| User Interface         | /frontend/src/        |
| Server Logic           | /server/              |
| Engine & APIs          | /engine/src/          |
| Engine Bindings Python | /engine/engine.pyi    |
| Client APIs            | /frontend/client/src/ |
|------------------------+-----------------------|

Building
--------
* For client, use `bun run dev`. The Rust module will be automatically
  compiled and bundled, and hot-reload enabled Vite starts serving on
  localhost:5173/. 
* For server, use `./gang run`. The Rust module will be compiled,
  the Python binding generated, the wheel built and installed automatically.
  `server/main.py` is subsequenly called, with CWD=/server/.

Licensing & Copyright
---------------------
Copyright (c) 2023-2024 Team Falco.

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
