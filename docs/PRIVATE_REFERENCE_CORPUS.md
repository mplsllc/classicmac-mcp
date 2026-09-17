# Private Reference Corpus

## Purpose

ClassicMacMCP may use user-owned historical manuals, SDK documentation, books, headers, samples, and release notes as a private follow-up corpus without redistributing those materials or allowing them to override verified project knowledge.

## Source classes

Private reference material is classified before indexing:

- `primary_vendor_documentation`
- `vendor_header_or_sdk`
- `vendor_sample_code`
- `historical_book`
- `cross_version_reference`

Each source records title, vendor/author, revision/version when known, applicability, repository/storage location, and redistribution policy.

## Retrieval behavior

Private reference retrieval is not the first automatic coding context.

Default target-programming order is:

1. canonical knowledge;
2. exact project/toolchain/hardware evidence;
3. applicable primary vendor documentation;
4. historical secondary references;
5. general model/external knowledge.

A private-source hit always returns `canonical_knowledge: false` and an evidence/source class.

## Structured manuals

When both HTML and TXT representations exist, prefer:

- HTML section/page structure for semantic chunk boundaries;
- TXT for broad full-text fallback;
- original PDF/media as archival verification where available.

Do not chunk structured manuals only by arbitrary token count when chapter/section/API boundaries can be recovered.

## Multipart manuals

Multiple files may represent one logical source. The source registry records ordered parts. Search results cite the logical manual identity and physical part/path.

Example: `SDKAPIRM.txt` and `SDKAPIRM2.txt` are one IDE 5.1 SDK API Reference.

## Code examples

Vendor/book sample code is not automatically compatible target code. Examples retain language/toolchain context and are excluded from automatic C89 implementation retrieval unless explicitly verified or reduced to a reviewed compatibility fact.

## Promotion

A reference statement may become canonical only after scope is established and the claim is reviewed. Exact-version headers or controlled CodeWarrior/hardware behavior may corroborate or contradict the reference.

Conflicts are retained rather than flattened.