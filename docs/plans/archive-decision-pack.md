# حزمة قرارات الأرشفة — 19 مرشحًا بالتحقق الحي (S3-T5، بنود 11 و14 و15)

> التاريخ: 2026-10-08 | **الأرشفة نفسها قرار مالك حصري** — هذه الحزمة تجهز الدليل والأوامر فقط.
> كل سطر تحقق حي ضد `GET /repos/{owner}/{repo}` وقت التوليد.
> التصنيفان من الجرد الجنائي (PORTFOLIO_INVENTORY.md): Duplicate ‏7 + Dead ‏13 —
> ملاحظة: المرشحون الفعليون 19 (بندي medical-ocr-trainer-hf متقاطعان بين الفئتين في الجرد).

## أوامر التنفيذ الجاهزة (بعد تفويض المالك، فئة فئة)

```bash
# فئة Duplicate — البندان غير المؤرشفين فقط (البقية مؤرشفون مسبقًا):
gh repo archive DrAbdulmalek/translation-core --yes
gh repo archive DrAbdulmalek/omni-medical-suite_dict --yes
# فئة Dead — البنود غير المؤرشفين (تُنفذ دفعة واحدة بعد موافقة جماعية موثقة):
```

## الجدول الحي الكامل

| المستودع | الفئة | مؤرشف الآن؟ | آخر دفع | الخلف المقترح | الإجراء | التراجع |
|---|---|---|---|---|---|---|
| `translation-core` | Duplicate | ❌ لا | 2026-10-04 | medical-translation-bot (توحيد الوظيفة) | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `omni-medical-suite_dict` | Duplicate | ❌ لا | 2026-10-04 | omni-medical-dictionaries | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `medical-translation-knowledge` | Duplicate | ✅ نعم | 2026-10-03 | translation-knowledge-base | لا إجراء — مؤرشف (يُقفل البند) | — |
| `translation-book-intake` | Duplicate | ✅ نعم | 2026-10-03 | medical-translation-intake | لا إجراء — مؤرشف (يُقفل البند) | — |
| `sync-github` | Duplicate | ✅ نعم | 2026-10-03 | repo-sync-toolkit (نصّت الخطة أرشفته نهائيًا) | لا إجراء — مؤرشف (يُقفل البند) | — |
| `omni-medical-workspace` | Duplicate | ✅ نعم | 2026-10-03 | zai-workspace / workspace-scripts-archive | لا إجراء — مؤرشف (يُقفل البند) | — |
| `medical-ocr-trainer` | Duplicate | ✅ نعم | 2026-07-07 | medical-ocr-trainer-hf (أبقِ أحدهما — الأحدث حيًا) | لا إجراء — مؤرشف (يُقفل البند) | — |
| `zai-workspace` | Dead | ❌ لا | 2026-10-05 | — (أرشفة فورية مقترحة) | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `medical-ocr-trainer-hf` | Dead | ❌ لا | 2026-10-04 | — (قرار أبقِ-واحدًا مقابل medical-ocr-trainer) | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `medical-ocr-archived` | Dead | ✅ نعم | 2026-10-03 | — | لا إجراء — مؤرشف (يُقفل البند) | — |
| `reset-net` | Dead | ❌ لا | 2026-09-01 | — | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `medical-ocr-demo` | Dead | ❌ لا | 2026-08-02 | — | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `OmniFile_Processor` | Dead | ❌ لا | 2026-08-01 | — (أو قرار إحياء P3) | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `radiology-ai-platform` | Dead | ❌ لا | 2026-08-01 | — | **READY_FOR_ARCHIVE** — بانتظار تفويض | `gh repo unarchive` |
| `medical-ocr-benchmarks` | Dead | ✅ نعم | 2026-07-07 | — | لا إجراء — مؤرشف (يُقفل البند) | — |
| `scanner-fixer` | Dead | ✅ نعم | 2026-07-07 | — | لا إجراء — مؤرشف (يُقفل البند) | — |
| `medical-ocr-training-hub` | Dead | ✅ نعم | 2026-07-07 | — | لا إجراء — مؤرشف (يُقفل البند) | — |
| `arabic-medical-ocr-baseline` | Dead | ✅ نعم | 2026-07-07 | — | لا إجراء — مؤرشف (يُقفل البند) | — |
| `medical-handwriting-ocr` | Dead | ✅ نعم | 2026-07-07 | — | لا إجراء — مؤرشف (يُقفل البند) | — |

## الخلاصة العددية (حية)

- مؤرشف مسبقًا (يُقفل بندُه دون حركة): **11**
- ينتظر تفويض أرشفة (READY_FOR_ARCHIVE): **8**
- تفويض مقترح للمالك: فئة Duplicate أولًا (2 بنود) ثم Dead دفعة جماعية موثقة —
  انظر OD-006 في owner-decision-queue.md. التراجع عن أرشفة ممكن عبر `gh repo unarchive`
  (التراجع متاح — لكن يبقى قرارًا حصريًا للمالك).
