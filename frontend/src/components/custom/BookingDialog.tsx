import React, { useState } from 'react';
import { BookingForm, Lab } from '@/lib/types';
interface Props { open: boolean; onClose: () => void; lab: Lab | null; period: number; onSubmit: (data: BookingForm) => void; }
export const BookingDialog: React.FC<Props> = ({ open, onClose, lab, period, onSubmit }) => {
  if (!open || !lab) return null;
  const [form, setForm] = useState<BookingForm>({ course: '', class: '', reason: '调课', content: '' });
  const handleSubmit = (e: React.FormEvent) => { e.preventDefault(); onSubmit(form); onClose(); };
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-white p-6 rounded-lg w-96" onClick={e => e.stopPropagation()}>
        <h3 className="text-xl font-bold mb-4">预约 {lab.name} - 第{period}节</h3>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input className="w-full border p-2 rounded" placeholder="课程名称" value={form.course} onChange={e => setForm({...form, course: e.target.value})} required />
          <input className="w-full border p-2 rounded" placeholder="班级" value={form.class} onChange={e => setForm({...form, class: e.target.value})} required />
          <select className="w-full border p-2 rounded" value={form.reason} onChange={e => setForm({...form, reason: e.target.value})}>
            <option>调课</option><option>补课</option><option>课设</option>
          </select>
          <textarea className="w-full border p-2 rounded" placeholder="实验内容" value={form.content} onChange={e => setForm({...form, content: e.target.value})} />
          <div className="flex justify-end gap-2">
            <button type="button" className="px-4 py-2 border rounded" onClick={onClose}>取消</button>
            <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">提交申请</button>
          </div>
        </form>
      </div>
    </div>
  );
};