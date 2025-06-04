# rdlevel_parse

A parser for Rhythm Doctor's JSON dialect.

# Background

Most modern RD levels are compliant JSON, but older levels sometimes have
divergences. Part of Rhythm Café's design goals is to support _all_ levels,
and therefore we have to be able to parse these.

**Newlines do not need to be escaped in strings**

```
{
 "key": "this is a valid
value in an rdlevel
even though it has newlines"
}
```

**Objects and arrays can have trailing commas, including the root object**

```
{
 "key": "aewfawefwae",
 "array": [1, 2, 3, 4, 5],
},
```

**Key pairs in objects can be seperated by whitespace**:

```
{"key": 2, "key2": 3 "key3": 4, "key4": [1, 2, 3] "key5": "hello world"}
```

**Key pairs in objects can be implicitly continued**:

```
{"key": 2"key2": 3"key3": 4}
```

# Implementation

This is a modified version of [naya](https://github.com/danielyule/naya) to add the relevant
extra parsing needed.  


# Install

Refer to installation steps in the [root-level README](../../README.md).


# Usage

`python -m rdlevel_parse <path to file>`

or:

`cat <path to file> | python -m orchard.parse`

# Testing

`pytest server/rdlevel_parse`