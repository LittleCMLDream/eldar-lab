import React from 'react';
import { Lab, Booking } from '@/lib/types';
interface Props { labs: Lab[]; bookings: Booking[]; week: number; day: number; onClick: (lab: Lab, period: number) => void; }
export const TimeGrid: React.FC<Props> = ({ labs, bookings, week, day, onClick }) => {
  const getStatus = (labId: number, p: number): { status: string; info?: string } => {
    const match = bookings.find(b => b.lab_id === labId && b.week === week && b.day === day && p >= b.start && p <= b.end);
    return match ? { status: match.status, info: match.course_name } : { status: 'free' };
  };
  if (labs.length === 0) return <div className="p-8 text-center text-gray-400">暂无实验室数据，请先导入课表或添加实验室</div>;
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="border p-2 bg-gray-100 sticky left-0 z-10 w-36 text-left pl-3">实验室</th>
            {[...Array(12)].map((_, i) => <th key={i} className="border p-2 bg-gray-100 w-10 text-xs">{i + 1}</th>)}
          </tr>
        </thead>
        <tbody>
          {labs.map(lab => (
            <tr key={lab.id}>
              <td className="border p-2 font-medium bg-gray-50 sticky left-0 z-10 text-xs pl-3">
                {lab.name}<div className="text-gray-400 text-[10px]">{lab.building}{lab.room_number}</div>
              </td>
              {[...Array(12)].map((_, i) => {
                const { status, info } = getStatus(lab.id, i + 1);
                const color = status === 'occupied' ? 'bg-red-100 text-red-700' : status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-50 text-green-600 cursor-pointer hover:bg-green-200';
                return (
                  <td key={i} className={`border p-1 text-center text-xs ${color}`} title={info || ''} onClick={() => status === 'free' && onClick(lab, i + 1)}>
                    {status === 'free' && '+'}
                    {status !== 'free' && '🔒'}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex gap-4 mt-2 text-xs text-gray-500">
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-green-50 border border-green-200"></div> 空闲 (点击预约)</span>
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-red-100 border border-red-200"></div> 课表/预约占用</span>
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-yellow-100 border border-yellow-200"></div> 待审批</span>
      </div>
    </div>
  );
};
