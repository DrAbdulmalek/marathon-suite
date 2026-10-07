# حملة medical-sources — مصادر الحصاد الطبي/الثنائي اللغة

> **المصدر:** محادثة DeepSeek `48pdrk6jj2uqy2li1c` (38 رسالة) — جمع المالك
> لمصادر النشرات الدوائية العربية والقواميس ثنائية اللغة ومصادر TEDx
> والتدريبات، بطلب صريح: «اجمع كل المصادر المتاحة في ملف واحد لأعطيه
> للتطبيق الذي ينزل المعلومات».
>
> **الحالة: `pending_wiring`** — المصادر موثقة وجاهزة، لكن لم تُكتب لها
> workers حصاد بعد (نفس نمط قرارات المالك الموثقة في حملتي ortho/translation).

## الملفات

| الملف | المحتوى | الصيغة |
|---|---|---|
| `data/arabic_pharma_consolidated.txt` | **الملف الموحد** — كل شركات الأدوية العربية ذات النشرات الثنائية (سورية/أردنية/مصرية/سعودية/…) | نص سطر-لكل-رابط — جاهز للتطبيق المنزِّل مباشرة |
| `data/hama_pharma_leaflets.txt` | روابط تحميل نشرات حماة فارما المباشرة (attachment download) | نص |
| `data/bilingual_dictionaries_books.txt` | قواميس وكتب ثنائية اللغة (Al-Mawrid, Hans Wehr, Lane, Oxford…) — archive.org وغيرها | نص |
| `data/syrian_pharma_companies.md` | جدول الشركات السورية + حالة توفر النشرات الثنائية | markdown |
| `data/tedx_sources.md` | مصادر TEDx (قنوات/playlist/صفحة المترجمين العرب) | markdown |
| `data/subtitle_downloaders.md` | منزلو الترجمة ثنائية اللغة (ted2srt/downsub/amara) | markdown |
| `data/training_corpora.md` | مدونات تدريب الترجمة (OPUS/UNCorpus/manythings…) | markdown |

## العلاقة بالمنظومة

- **الحصاد**: نمط `campaigns/translation/web_sources.yaml` نفسه — عند كتابة
  worker لأي مصدر، تُرفع حالته هنا إلى `active` مع اسم الـ worker في `note`.
- **معالجة النشرات**: النشرات الثنائية (AR/EN PDF) تغذي
  `medical-translation-intake` (استخراج مصطلحات) و`ocr-core` (ميثاق 18 قاعدة).
- **القواميس**: تحقق أولًا من `dictionaries-csv` (466,670 مدخلًا محوَّلة
  مسبقًا) قبل أي تحويل مكرر — dedup بالمحتوى.
- **TEDx/ted2srt**: يكمل `marathon_ted_pipeline` (ted2srt_py موجود فيه).

## ملاحظات أمان/جودة

- الروابط جُمعت من بحث ويب (2026-09/10) — **تحقق منAvailability قبل الحصاد**
  (روابط attachment قد تتغير).
- لا تُرفع الملفات المحصَّلة إلى git — تُنشر في قناة الهدف
  (@DrMalekDrive لحملة الترجمة) وفق قواعد الحملات الأخرى.
