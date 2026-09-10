# English translation maintenance

The Japanese HTML pages are the source for the seven English pages in `en/`.
`en.json` maps complete Japanese text segments to their English translations.

After editing a Japanese page, add or update its translation, then run:

```sh
python scripts/build_english.py
python scripts/check_translations.py
```

The generator stops on untranslated Japanese text. It generates static HTML,
paired language links and search metadata. Visitors do not need JavaScript to
read either language or switch pages. `js/language.js` additionally preserves
the current section when switching languages.

Translate archived speaker affiliations as recorded at that meeting. Preserve
program times, fees and the original artwork. Talk and project titles are
English translations of the Japanese site text, not new official titles.

Selected name references consulted:

- Maina Sogabe: https://nrid.nii.ac.jp/ja/nrid/1000080788951/
- Hirohiko Kohjitani: https://medtech.m.u-tokyo.ac.jp/introduction/hirohiko-kohjitani/
- Raiki Yoshimura, Shoya Iwanami, Daiki Tatematsu: https://iblab.bio.nagoya-u.ac.jp/members
- Koichiro Majima, HiTSeq presentation at ISMB/ECCB 2023: https://www.youtube.com/watch?v=7bSAHQuHTG4
- Yu Teshima: https://scholar.google.com/citations?hl=en&user=i1W_QkoAAAAJ
