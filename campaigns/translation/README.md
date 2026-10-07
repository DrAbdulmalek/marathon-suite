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
| المنفّذ | **gdrive-telegram-tools → `translation_harvest.py`** (المحرك المخصص، التزام 3718bea — 2026-10-07)؛ السلف `tg_forward_to_channel.py` v2.1 موقوف كاحتياط ويبقى متسقاً مع السجل |
| سجل المنع | `sent_index.json` — مفتاح `stem::size` في `state/translation_harvest/`، مُبذَّر من سجل الماراثون القديم (channel_inventory + sent_files_new)؛ كل إرسال جديد يُلحق بالسجلين |
| البذر الأولي | `seed_forward_state.py` يزرع سجل المنع من جرد القناة (`channel_inventory.jsonl`) — «المضاف سابقاً» لا يُعاد |
| الاستئناف | `progress.json` يُحفظ ذرّياً بعد كل دفعة؛ مؤشران لكل مصدر: `band` (ceil/floor بتصميم العظام) و`asc` (استئناف تصاعدي للمصادر المُرحّلة)؛ مسح boundary-exact — لا رسالة تُعالَج مرتين؛ FloodWait → موعد مؤجل + خروج نظيف |
| المصادر المحمية | noforwards → وضع النسخ العميق (تنزيل ثم رفع، سقف 150MB) |
| الاكتشاف | ترويسات fwd_from (hop≤2) مع فلترة مفردات الترجمة وبوابة خصوصية Issue #1 → `state/translation_harvest/discovered.jsonl` |
| طبقة الويب | createdres (789 PDF) + مكتبة نور + MedlinePlus |

## السجلات

- `sources.yaml` — **88 مصدر تيليجرام، كلها نشطة ومربوطة** (2026-10-07):
  86 من قائمة الماراثون الموثقة + القناتان المربوطتان من بحث 2026-10-07
  (`@medicalrefrencess` 671 وثيقة في أول جولة، `@medicalegypt` 41 وثيقة —
  وضع `doc`، التزام 3718bea).
  ملاحظة: إجمالي المصادر المسجلة عبر كل سكربتات الجرافة (register_*, probe_*)
  ~263؛ الـ86 النشطة هنا هي المتصلة فعلياً بمحرك التحويل.
- `web_sources.yaml` — 3 جرافات ويب.

### التحديث

عند إضافة مصادر لقائمة PRIMARY في السكربت: حدّث `sources.yaml` بالتوازي،
وحدّث `stats.telegram_total`. عدّد الاختبار `test_translation_registry_matches_forwarder_primary`
إذا تغير العدد.

## مصادر موثقة جديدة (بحث 2026-10-07) — الربط مكتمل

تحقق مباشر من صفحات t.me (2026-10-07) أضاف مصدرين — **مربوطان الآن بالمحرك
المخصص** `gdrive-telegram-tools/translation_harvest.py` (التزام 3718bea،
2026-10-07): حُلّتا كقناتَي broadcast وأُضيفتا لبذرة الحلّال بوضع `doc`،
ورُفعت حالتهما إلى active مع حقل `wired_verified`:

| المعرّف | المشتركون | الوصف |
|---|---|---|
| @medicalrefrencess | 53 042 | مراجع وكتب وبرامج طبية (قناة منذ 2018) |
| @medicalegypt | 17 307 | Medical Books Pdf — كتب طبية عربية/أجنبية |

مستبعَد موثق: @books_medical — حساب مستخدم وليس قناة (زر Send Message بدل
Preview channel في t.me)؛ الحسابات غير قابلة للسحب الآلي.
## التصحيح: إزالة campaigns/ortho_homs.yaml

الملف السابق `campaigns/ortho_homs.yaml` كان يسجّل مصادر المسارد والقواميس
(arabic-medical-glossary، omni-medical-dictionaries) تحت هدف **@ortho_homs** —
خطأ سياق موثّق في تدقيق اللوحة (تعليق 5992647557، مصحح في fc1e02f):
تلك المصادر تنتمي لحملة الترجمة هذه (@DrMalekDrive)، بينما @ortho_homs هي
هدف حملة العظام المستقل (campaigns/ortho). حُذف الملف واستُبدل بهذا التعريف،
والمرجعان المذكوران مسجّلان في واجهة اللوحة ضمن `MEDICAL_GLOSSARY_SOURCES`.