export default function ConsumerGuidePage() {
  return (
    <div className="max-w-4xl mx-auto space-y-6 text-sm leading-relaxed">
      <h1 className="text-2xl font-bold">الدليل التقني للمستهلك الجزائري</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
          <h2 className="font-bold text-emerald-600">1. الرغوة (Mousse)</h2>
          <p>تُقاس الكثافة بـ كغ/م³. رغوة D35 وD36 وHR مناسبة للاستخدام العائلي اليومي، بينما D20–D28 تفقد مرونتها سريعاً في المقاعد الرئيسية.</p>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
          <h2 className="font-bold text-emerald-600">2. الخشب والهيكل</h2>
          <p>خشب الزان (Hêtre) والبلوط (Chêne) المجفف أفضل في نقاط الضغط من الـ MDF والخشب الحبيبي (Aggloméré).</p>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
          <h2 className="font-bold text-emerald-600">3. الأقمشة والتعليق</h2>
          <p>الأقمشة المضادة للبقع (`Anti-tache` / `Déperlant`) مع نوابض `Nosag` تضمن عمراً أطول وسهولة تنظيف للعائلات.</p>
        </div>
        <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
          <h2 className="font-bold text-emerald-600">4. الدينار مقابل السنتيم</h2>
          <p>احرص دائماً على التحقق من السعر النهائي بالدينار الجزائري (12 مليون سنتيم = 120,000 دج) مع احتساب مصاريف النقل والتركيب.</p>
        </div>
      </div>
    </div>
  );
}
