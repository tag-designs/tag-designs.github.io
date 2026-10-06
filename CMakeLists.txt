cmake_minimum_required(VERSION 3.10)

project(tag-designs-docs LANGUAGES NONE)

#[[
  The documentation site is MkDocs Material; `mkdocs build` is the whole
  build. This file exists so the site can be built the same way as the rest
  of the project, and to keep the TikZ -> SVG pipeline, which is independent
  of the site generator.

  Targets:
    docs        build the site into ${CMAKE_CURRENT_BINARY_DIR}/site
    images-svg  regenerate the TikZ diagrams (needs pdflatex and pdf2svg)
]]

find_program(MKDOCS_EXECUTABLE NAMES mkdocs)

if(MKDOCS_EXECUTABLE)
  add_custom_target(docs
    COMMAND ${MKDOCS_EXECUTABLE} build --strict
            --site-dir "${CMAKE_CURRENT_BINARY_DIR}/site"
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Building the documentation site with MkDocs")
else()
  message(STATUS
    "mkdocs not found; the docs target is unavailable. "
    "Install it with: python3 -m pip install -r requirements.txt")
endif()

#[[
  TikZ sources for the architecture diagrams. The SVGs they produce are
  committed under docs/, so this only needs running when a diagram changes.
  Unrelated to the site generator: it was the same under Hugo.
]]

file(GLOB TIKZ_SOURCES ${PROJECT_SOURCE_DIR}/tikz/*.tex)
set(image-out-directory "${CMAKE_CURRENT_SOURCE_DIR}/docs/images-svg")
file(MAKE_DIRECTORY ${image-out-directory})

add_custom_target(images-svg)

foreach(f ${TIKZ_SOURCES})
  get_filename_component(fname ${f} NAME_WLE)

  add_custom_command(
    OUTPUT "${fname}.pdf"
    COMMAND pdflatex -output-directory="${CMAKE_CURRENT_BINARY_DIR}"
            -interaction=batchmode "${f}"
    BYPRODUCTS "${CMAKE_CURRENT_BINARY_DIR}/${fname}.log"
               "${CMAKE_CURRENT_BINARY_DIR}/${fname}.aux"
    DEPENDS ${f})

  add_custom_command(
    OUTPUT "${fname}.svg"
    COMMAND pdf2svg "${fname}.pdf" "${fname}.svg"
    COMMAND cmake -E copy_if_different "${fname}.svg" "${image-out-directory}"
    DEPENDS "${fname}.pdf")

  add_custom_target("${fname}-tikz" DEPENDS ${fname}.svg)
  add_dependencies(images-svg "${fname}-tikz")
endforeach()
