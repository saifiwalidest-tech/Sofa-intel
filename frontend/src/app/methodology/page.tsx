export default function MethodologyPage() {
  return (
    <div className="max-w-4xl mx-auto space-y-6 text-sm leading-relaxed">
      <h1 className="text-2xl font-bold">المصادر ومنهجية التقييم (Sofa Quality Index)</h1>
      <p>
        يعتمد مؤشر الجودة في منصة <strong>SOFA INTEL DZ</strong> على 100 نقطة قابلة للتخصيص: الرغوة (25)، الهيكل والخشب (25)، القماش (15)، التعليق (15)، التشطيب (10)، والضمان (10).
      </p>
      <div className="rounded-2xl border border-wood-500/25 bg-white dark:bg-navy-900 p-5 space-y-2">
        <h2 className="font-bold">قواعد الشفافية ومنع التضليل</h2>
        <ul className="list-disc mr-5 space-y-1">
          <li>لا يتم افتراض أن ذكر «D36» في الإعلان يعني كثافة حقيقية 36 كغ/م³ دون شهادة تقنية.</li>
          <li>المعلومات المفقودة لا تتحول إلى أصفار، بل تُحسب ضمن نطاق الجودة المحتمل (`min–max`) ونسبة اكتمال البيانات.</li>
          <li>جميع العروض التجريبية موسومة بوضوح بعلامة `DEMO DATA` ولا تُعرض كعروض حية.</li>
        </ul>
      </div>
    </div>
  );
}
