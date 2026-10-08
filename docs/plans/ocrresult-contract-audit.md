# تدقيق عقد OCRResult — التوحيد بين ocr-core وarabic-medical-handwriting (S2-T3، بند 13)

> التاريخ: 2026-10-08 | الدليل: قراءة المصدرين الحيين وقت التدقيق.
> `ocr-core/src/ocr_core/engines/base.py:15` مقابل `arabic-medical-handwriting/ocr/contract.py`.

## جدول الفروق الثمانية الموثقة

| # | المحور | ocr-core (النواة) | arabic-medical-handwriting (AMH) | الأثر |
|---|---|---|---|---|
| 1 | زمن المعالجة | `processing_time: float = 0.0` (وحدة غير موثقة) | `duration_ms: float = 0.0` (ملي ثانية صراحة) | اسم + وحدة — خطر أخطاء مقارنة قياس |
| 2 | مواضع الكلمات | ❌ لا يوجد | `words: list[WordBox]` (text/bbox/confidence) | الطبقة العليا تحتاجه للمراجعة البشرية |
| 3 | اللغة | ❌ | `language: str = "ar"` | مطلوب للمسار الذهبي عربي أولًا |
| 4 | النص الخام | ❌ | `raw_text: str` (قبل التنظيف) | أساس قياس CER العادل |
| 5 | تحذيرات | ❌ (error فقط) | `warnings: list[str]` + `error` | فقدان سياق في النواة |
| 6 | dict بيانات | `meta` | `metadata` | تعارض تسمية مباشر |
| 7 | صفحات | `pages: int = 1` | ❌ | مطلوب لـ PDF متعدد الصفحات |
| 8 | engine الافتراضي | `""` | `"unknown"` + `created_at` + `is_empty/word_count/summary` | اختلاف معلوماتية بسيط |

**سياسة الثقة**: النواة وحدها توثّق «0.0 = مجهول، يُمنع اختلاق رقم» (R15) — يجب تعميمها على الطرفين حرفيًا.

## الشكل القانوني المقترح (الأساس: النواة + إضافات AMH)

```python
@dataclass
class OCRResult:
    text: str = ""
    engine: str = "unknown"
    confidence: float = 0.0      # 0.0 = unknown — never a fabricated score (R15)
    duration_ms: float = 0.0     # وحدة صريحة — يعوض processing_time
    error: Optional[str] = None
    pages: int = 1
    meta: dict = field(default_factory=dict)          # الاسم القانوني (كانت metadata في AMH)
    words: list[WordBox] = field(default_factory=list) # إضافة AMH للنواة
    language: str = "ar"
    raw_text: str = ""
    warnings: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def ok(self) -> bool: return self.error is None          # من النواة
    @property
    def processing_time(self) -> float: return self.duration_ms  # alias تقادم في النواة
    # + is_empty / word_count / summary من AMH
```

**التسمية الفائزة**: `meta` (تسمية النواة) و`duration_ms` (الاسم الموثق الوحدة) —
`metadata`/`processing_time` يبقيان alias تقادم في AMH/النواة دون كسر مستهلكين.

## خطة الترحيل الثلاثية (قابلة للعكس كلية)

1. **توحيد التعريف** في `base.py` + `contract.py` (نفس الحقول حرفيًا) + alias تقادم.
2. **اختبار تكافؤ العقد** (`test_contract_parity.py` في المستودعين): يفشل فورًا إذا
   اختلفت مجموعات الحقول أو قيمها الافتراضية — يمنع الانزلاق مستقبلًا.
3. **تحديث نقاط الإنشاء** (engines/adapter) لملء الحقول الجديدة قدر الإمكان
   (words حيث يتوفر، raw_text دائمًا) — كل خطوة PR مستقل قابل للـ revert.

## لماذا لم يُنفَّذ التوحيد الكودي في هذه الموجة؟

اختيار أسماء الحقول القانونية **قرار معماري** (العقد §12: أي تغيير معماري يتطلب دليلًا
وقرارًا معماريًا صريحًا). الشكل أعلاه = المقترح المؤهل؛ اعتماده بند قرار في
owner-decision-queue (مرفق OD-004B)، وبعده تُنفَّذ الخطوات الثلاث آليًا دون انتظار.
