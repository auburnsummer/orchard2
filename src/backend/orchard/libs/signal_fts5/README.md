
1. cd into `Signal-FTS5-Extension`
2. `cargo rustc --lib --features extension --crate-type cdylib`
3. a file in directory `./target/release` is created called `libsignal_tokenizer.so`
4. load it, e.g. `.load ./libsignal_tokenizer.so signal_fts5_tokenizer_init`, noting the init function name must be specified
5. pass as tokenizer option, see the other README