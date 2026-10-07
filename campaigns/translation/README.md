# حملة الترجمة — مكتبة DrMalekDrive

> تعريف رسمي لحملة سحب كتب الترجمة والمراجع والمسارد إلى **@DrMalekDrive** —
> كانت الحملة تعمل سابقاً من سكربتات مبعثرة في tg-campaign-toolkit بلا تعريف معلن؛
> هذا المجلد يوحّدها بنفس بنية حملة العظام (campaigns/ortho).

## القناة الهدف

- **@DrMalekDrive** (telegram_id 3913901632) — ~29.5 ألف رسالة / ~150GB.
- دورها: وجهة كل المحتوى المسحوب: كتب ترجمة، قواميس ثنائية، مسارد طبية،
  نشرات أدوية، كتب إنجليزية/تعليمية.
- القناة موحّدة في ثلاثة مواضع في واجهة اللوحة (`layout.tsx`، `page.tsx`،
  `preview-dialog.tsx`) وفي `MEDICAL_CHANNEL_TARGET` (campaign: medical-translation)
  بعد تصحيح fc1e02f لبواقي تعارض @ortho_homs.

## المعمارية

| المكوّن | المكان |
|---|---|
| المنفّذ | tg-campaign-toolkit → `scripts/tg_forward_to_channel.py` (v2.1، المحرك `marathon` في اللوحة) |
| سجل المنع | `sent_index.py` — مفتاح (اسم الملف + الحجم بالبايت) عبر `state/forward/*.jsonl` |
| البذر الأولي | `seed_forward_state.py` يزرع سجل المنع من جرد القناة (`channel_inventory.jsonl`) — «المضاف سابقاً» لا يُعاد |
| الاستئناف | `progress.json` يُحفظ ذرّياً بعد كل دفعة؛ FloodWait → موعد مؤجل + إيقاء |
| المصادر المحمية | noforwards → وضع النسخ العميق (تنزيل ثم رفع، سقف 150MB) |
| الاكتشاف | ترويسات fwd_from (hop≤2) مع فلترة مفردات الترجمة → `discovered.jsonl` |
| طبقة الويب | createdres (789 PDF) + مكتبة نور + MedlinePlus |

## السجلات

- `sources.yaml` — **86 مصدر تيليجرام** مولّد آلياً من قائمة PRIMARY في السكربت
  (كل مصدر: handle فعلي + mode: all/doc/media + علامة filtered للمفلترة).
  ملاحظة: إجمالي المصادر المسجلة عبر كل سكربتات الجرافة (register_*, probe_*)
  ~263؛ الـ86 هنا هي المتصلة فعلياً بمحرك التحويل.
- `web_sources.yaml` — 3 جرافات ويب.

### التحديث

عند إضافة مصادر لقائمة PRIMARY في السكربت: حدّث `sources.yaml` بالتوازي،
وحدّث `stats.telegram_total`. عدّد الاختبار `test_translation_registry_matches_forwarder_primary`
إذا تغير العدد.

## التصحيح: إزالة campaigns/ortho_homs.yaml

الملف السابق `campaigns/ortho_homs.yaml` كان يسجّل مصادر المسارد والقواميس
(arabic-medical-glossary، omni-medical-dictionaries) تحت هدف **@ortho_homs** —
خطأ سياق موثّق في تدقيق اللوحة (تعليق 5992647557، مصحح في fc1e02f):
تلك المصادر تنتمي لحملة الترجمة هذه (@DrMalekDrive)، بينما @ortho_homs هي
هدف حملة العظام المستقل (campaigns/ortho). حُذف الملف واستُبدل بهذا التعريف،
والمرجعان المذكوران مسجّلان في واجهة اللوحة ضمن `MEDICAL_GLOSSARY_SOURCES`.
