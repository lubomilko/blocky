# Introduction 
Blocky is a simple Python pseudo-templating engine allowing generation of various types of text-based content. It was primarily developed for C source file generation, but can be used for other programming languages, data files or strings too.

Blocky is based on the following principles:

* **Logic-less templates** - Templates contain primarily the content needed to be generated. Logic to set the data into the variable parts of a template is defined separately.
* **No custom templating language** - Rendering logic is defined in Python script file that uses objects provided by the blocky module.
* **No custom data model** - Since Python is used, any format or type of input data can be used to fill the variable parts of templates or to control the rendering logic.
* **Minimalism** - Just one small python module without any dependencies on complex external modules. All of the main functionalities are provided by one main class.
* **Versatility** - Blocky can be used for source code generation for any common programming languages (C, C++, C#, Java, Javascript, Python, SQL, HTML, CSS, etc.) and also for generation of various text files (TXT, CSV, XML, JSON, MD, RST, etc.). Data to be used in templates can come from any source.


# Functional Overview
Blocky module is not a typical full templating engine, since it is not parsing and executing the templating language provided in the template. The logic of the file generation heavily relies on the separate template-specific custom Python script provided by the template creator. Following diagram illustrates the processing flow of the file generation:

```

	      input data
	           |
	TEMPLATE   |  
	     |     |
	     V     V
	TEMPLATE FILLING SCRIPT <-> blocky module
	           |
	           V
	   generated content
```

The static ``TEMPLATE FILLING SCRIPT`` uses functionalities provided by the imported blocky module to fill the variable parts of the static ``TEMPLATE`` with the variable content of the ``input data`` to generate the output ``generated content``.
