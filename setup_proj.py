#!/usr/bin/python3

import argparse
import os

parser = argparse.ArgumentParser(description='Create a new C/C++ project directory')
parser.add_argument('project_name', type=str, help='The name of the new project being created')


def main():
    args = parser.parse_args()
    project_name = args.project_name

    cwd = os.getcwd()
    project_dir = os.path.join(cwd, project_name)

    if os.path.isdir(project_dir):
        raise FileExistsError(f'{project_dir} already exists!')

    # Create folder
    os.mkdir(project_dir)
    source_dir = os.path.join(project_dir, 'src')
    os.mkdir(source_dir)
    
    # Create main file
    main_file_text = """#include <fmt/core.h>

int main([[maybe_unused]] int argc, [[maybe_unused]] const char* argv[])
{
    fmt::print("Hello, Rock!\\n");
}
"""
    with open(os.path.join(source_dir, 'main.cpp'), 'w') as f:
        f.write(main_file_text)

    cmake_file_text = f"""cmake_minimum_required(VERSION 3.23)
project({project_name})

include(FetchContent)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

FetchContent_Declare(fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG master
    GIT_SHALLOW ON
)
FetchContent_MakeAvailable(fmt)

add_executable({project_name} src/main.cpp)
set_property(TARGET {project_name} PROPERTY CXX_STANDARD 23)
if (CMAKE_BUILD_TYPE MATCHES Debug)
    target_compile_definitions({project_name} PRIVATE {project_name.upper().replace('-', '_')}_DEBUG)
endif()

target_compile_options({project_name} PRIVATE -Wall -Wextra -Wpedantic -Werror)

target_link_libraries({project_name} PRIVATE fmt::fmt)
"""

    with open(os.path.join(project_dir, 'CMakeLists.txt'), 'w') as f:
        f.write(cmake_file_text)

    gitignore_text = """# Prerequisites
*.d

# Compiled Object files
*.slo
*.lo
*.o
*.obj

# Precompiled Headers
*.gch
*.pch

# Compiled Dynamic libraries
*.so
*.dylib
*.dll

# Fortran module files
*.mod
*.smod

# Compiled Static libraries
*.lai
*.la
*.a
*.lib

# Executables
*.exe
*.out
*.app

# Generated Folders
build/**/*
"""

    with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
        f.write(gitignore_text)

    print(f'Successfully created {project_dir}!')


if __name__ == '__main__':
    main()

