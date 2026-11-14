# Handasa Ecosystem Hub

منصة خاصة لاكتشاف مشاريع GitHub العامة، إعداد ترشيحات للشراكات، وإنشاء مقترحات منح **تحتاج مراجعة وموافقة مسبقة**.

## المكونات

- `trending_scanner.py`: يستخدم GitHub public repository search API للبحث اليومي عن مشاريع AI وAgents وأدوات المطورين، مع النجوم والوصف واللغة والرخصة وتاريخ التحديث.
- `grants_manager.py`: يحسب مقترح منحة ويضعه `pending_review`؛ لا يدفع ولا يحول ولا يصل إلى محفظة.
- `ecosystem_sdk.py`: قالب GET للبيانات والإحصائيات، بلا صلاحية نقل أصول.
- `alerts.py`: قوالب Discord للإشعار فقط.
- `.github/workflows/ecosystem-daily.yml`: فحص يومي ورفع النتائج كـ Artifacts.

## أسرار ومتغيرات

### Secret اختياري

- `GITHUB_READ_TOKEN` — Token قراءة فقط لرفع حدود GitHub API، وليس مطلوبًا للبحث العام.
- `DISCORD_WEBHOOK` — للإشعارات بعد مراجعة بشرية؛ لا يوجد نشر تلقائي مفعّل في Workflow.

### Variable

- `GRANT_AMOUNT_USD` — قيمة مقترحة للتقييم فقط، لا تعني موافقة أو دفعًا. إذا لم تُضبط، ينشئ النظام تقرير `awaiting_configuration` بلا مبلغ أو مقترح تمويلي بدل فشل الفحص.

## ضوابط المنح

كل منحة تمر بالحالات التالية:

```text
candidate → due_diligence → pending_review → multisig_approved → paid_externally
```

المستودع ينفذ فقط مرحلتي الاكتشاف وإعداد المقترح. لا توجد مفاتيح خاصة أو signer أو تحويل أموال.

## قالب التكامل

`ecosystem_sdk.py` ينتج أوصاف طلبات قراءة فقط لإحصائيات المشروع. لا يرسل الطلبات ولا يمنح المشروع وصولًا إلى الأصول أو الأسرار.

## التشغيل

```bash
python -m unittest -v
python trending_scanner.py
python grants_manager.py
```

نتائج Workflow تحفظ كـ Artifacts لمدة 14 يومًا. يجب إجراء العناية الواجبة يدويًا قبل أي شراكة أو منحة، بما في ذلك مراجعة الترخيص، الأمان، النشاط، تضارب المصالح، والهوية.
