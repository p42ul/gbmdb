# GBMDB
## The Game Boy Music Database

This is a project based on the [NES Music Database](https://github.com/chrisdonahue/nesmdb) which attempts to follow a similar methodology for Game Boy games.

It is a work in progress, if you have any comments or suggestions please let me know!

## Getting started

1. Clone the repository (this guide assumes the folder is called *gbmdb*.
1. Inialize submodules using: `git submodule update --init --recursive`.
1. Compile the custom VGMPlay: `cd vgmplay/VGMPlay && make && cd ../..`.
1. Dump expressive characteristics to a file `vgmplay/VGMPlay/vgm2wav ${your_vgm_file} /dev/null > ${output_file}`

Here is an example of some expressive characteristics that have been extracted from the Pokemon theme song:

![Expressive characteristics of the Pokemon theme song](doc/example.png)

## To-do list:

- Create MIDI data from expressive characteristics
  - This will require investigating how to calculate "note-on" and "note-off" messages
- Sort through which expressive characteristics are most useful in a musical context
- Optimize file size of captured data
