# vitals

Extract metadata from a rdzip.

# Background

vitals grabs metadata using "facets", which are functions defined in the [facets directory](./facets).
Each facet function is responsible for a little bit of metadata. vitals calls these facet functions and builds
a final metadata object out of the result.

An important note is that vitals is deterministic based on the rdlevel. That is, it will always give the exact
same result if you give it the same rdzip. This means that all information must originate from the rdzip itself,
so for instance vitals determines the created date by the created date on the zip file, and not when it reads the file.

Facet functions have access to the following info:

 - The json representation of the rdlevel created by [rdlevel_parse](../rdlevel_parse/README.md)
 - The zipfile (a python [`zipfile.ZipFile`](https://docs.python.org/3/library/zipfile.html) object)
 - The file, as bytes
 - An optional TOML object which may be in the level

The TOML object is parsed based on the first Comment event in the rdlevel that has the text `#orchard` in it. It's
mainly used for overriding metadata where the facet heuristics may be incorrect. I haven't publicised this
functionality yet, so no levels use it as of now.