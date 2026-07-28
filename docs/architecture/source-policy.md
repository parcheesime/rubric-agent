# Source Policy

**Project:** Rubric Agent  
**Status:** Draft

---

# Purpose

Rubric Agent builds a reference corpus of educational materials from publicly available sources to support document interpretation, normalization, educational search, and future AI-assisted educational applications.

This policy defines the principles used to evaluate, collect, and maintain educational resources within the project.

Rather than maintaining a fixed list of approved repositories, this document establishes the criteria that guide source selection and collection practices as the project evolves.

---

# Source Selection Principles

Rubric Agent seeks to build a broad, diverse, and traceable corpus of educational materials.

Collection should prioritize educational value, provenance, reproducibility, and respect for content creators over the volume of collected documents alone.

Whenever possible, resources should be collected from their original publishers or official repositories.

---

# Preferred Source Types

Rubric Agent prioritizes educational resources from sources such as:

- Universities and colleges
- Open educational resource (OER) repositories
- Government educational organizations
- Public school districts
- Educational nonprofits
- Research institutions
- Official curriculum repositories
- Public institutional archives

Examples may include:

- MIT OpenCourseWare
- OAK OpenAPI
- University digital collections
- Institutional repositories
- Future approved educational sources

The project intentionally avoids depending on any single provider.

---

# Source Selection Criteria

Potential sources should be evaluated using several considerations.

## Educational Value

Resources should contribute meaningful instructional information such as:

- learning objectives
- assessment expectations
- instructional design
- educational structure
- curriculum planning
- classroom resources

---

## Provenance

The source should clearly identify, whenever available:

- institution
- publisher
- author or department
- publication or revision date
- repository identifier
- original URL

---

## Stability

Preferred sources provide stable access through:

- permanent URLs
- APIs
- repository identifiers
- IIIF manifests
- institutional archives

Stable sources improve reproducibility and future reprocessing.

---

## Licensing Transparency

Whenever available, licensing information should be preserved exactly as provided by the source.

Unknown licensing information should be recorded rather than inferred.

---

## Accessibility

Resources should be publicly accessible through normal means.

Rubric Agent should not intentionally bypass:

- authentication
- paywalls
- technical protections
- access controls

---

# Collection Methods

Collectors may retrieve educational materials through methods including:

- Public APIs
- Repository APIs
- IIIF manifests
- Public metadata feeds
- HTML pages
- Public document downloads

Collection methods should preserve source metadata whenever possible.

---

# Ethical Collection

Collectors should behave as respectful automated clients.

Collectors should:

- identify themselves when appropriate
- avoid unnecessary server load
- honor published rate limits
- avoid excessive request frequency
- retrieve only information needed for educational processing
- preserve attribution

Collection should support educational research and interoperability rather than large-scale content duplication.

---

# Source Metadata

Each collected resource should preserve available source metadata, including:

- Source URL
- Institution
- Publisher
- Collection
- Retrieval timestamp
- License information
- Document identifier
- Collector identifier
- Retrieval method

Additional metadata should be preserved whenever available.

---

# Unsupported Sources

Rubric Agent does not intentionally collect from sources that:

- require bypassing technical protections
- violate applicable terms governing access
- contain primarily personal or private educational materials
- lack sufficient provenance to support reproducible processing
- cannot be reasonably attributed

---

# Source Evolution

The set of supported educational repositories will evolve over time.

New sources should be evaluated according to the principles defined in this policy rather than by maintaining a static allowlist.

As Rubric Agent expands, additional source-specific documentation may be created to describe unique repository structures, APIs, metadata formats, or licensing considerations.

---

# Relationship to the Data Policy

This policy governs the acquisition of educational resources.

Once a resource has been acquired, its handling, storage, normalization, provenance, and downstream use are governed by the project's Data Policy.