
1. cd into `Signal-FTS5-Extension`
2. if it's empty you might need to do `git submodule update --init --remote --recursive`
2. `cargo rustc --lib --features extension --crate-type cdylib --release`
3. a file in directory `./target/release` is created called `libsignal_tokenizer.so`
   - if you need to build for a different architecture, you might need to move it into the right location since it will be placed in a different directory
4. load it, e.g. `.load ./target/release/libsignal_tokenizer signal_fts5_tokenizer_init`, noting the init function name must be specified
5. pass as tokenizer option, see the other README