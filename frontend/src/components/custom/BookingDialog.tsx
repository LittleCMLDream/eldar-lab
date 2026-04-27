import React, { useState } from 'react';
import { BookingForm, Lab } from '@/lib/types';
interface Props { open: boolean; onClose: () => void; lab: Lab | null; period: number; onSubmit: (data: BookingForm) => void; }
export const BookingDialog: React.FC<Props> = ({ open, onClose, lab, period, onSubmit }) => {
  if (!open || !lab) return null;
  const [form, setForm] = useState<BookingForm>({ course: '', class: '', reason: '调课', content: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: Record<string, string> = {};
    if (!form.course) newErrors.course = '必填';
    if (!form.class) newErrors.class = '必填';
    if (Object.keys(newErrors).length > 0) { setErrors(newErrors); return; }
    onSubmit(form); setForm({ course: '', class: '', reason: '调课', content: '' }); setErrors({});
  };
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white p-6 rounded-lg w-96 shadow-xl" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">预约 {lab.name}</h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-xl">&times;</button>
        </div>
        <p className="text-sm text-gray-500 mb-4">📅 第 {period} 节课</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input className={`w-full border p-2 rounded ${errors.course ? 'border-red-500' : ''}`} placeholder="课程名称" value={form.course} onChange={e => setForm({...form, course: e.target.value})} />
            {errors.course && <p className="text-red-500 text-xs mt-1">{errors.course}</p>}
          </div>
          <div>
            <input className={`w-full border p-2 rounded ${errors.class ? 'border-red-500' : ''}`} placeholder="班级" value={form.class} onChange={e => setForm({...form, class: e.target.value})} />
            {errors.class && <p className="text-red-500 text-xs mt-1">{errors.class}</p>}
          </div>
          <select className="w-full border p-2 rounded" value={form.reason} onChange={e => setForm({...form, reason: e.target.value})}>
            <option>调课</option><option>补课</option><option>课设</option><option>培训</option><option>其他</option>
          </select>
          <textarea className="w-full border p-2 rounded" rows={3} placeholder="实验内容 (可选)" value={form.content} onChange={e => setForm({...form, content: e.target.value})} />
          <div className="flex justify-end gap-2 pt-2">
            <button type="button" className="px-4 py-2 border rounded hover:bg-gray-50" onClick={onClose}>取消</button>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">提交申请</button>
          </div>
        </form>
      </div>
    </div>
  );
};
