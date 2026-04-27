import React from 'react';
import { Lab, Booking } from '@/lib/types';
interface Props { labs: Lab[]; bookings: Booking[]; week: number; day: number; onClick: (lab: Lab, period: number) => void; }
export const TimeGrid: React.FC<Props> = ({ labs, bookings, week, day, onClick }) => {
  const getStatus = (labId: number, p: number): string => {
    const match = bookings.find(b => b.lab_id === labId && b.week === week && b.day === day && p >= b.start && p <= b.end);
    return match ? match.status : 'free';
  };
  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm">
        <thead>
          <tr>
            <th className="border p-2 bg-gray-100 sticky left-0 z-10">实验室</th>
            {[...Array(12)].map((_, i) => <th key={i} className="border p-2 bg-gray-100 w-12">{i + 1}</th>)}
          </tr>
        </thead>
        <tbody>
          {labs.map(lab => (
            <tr key={lab.id}>
              <td className="border p-2 font-medium bg-gray-50 sticky left-0 z-10">{lab.name}</td>
              {[...Array(12)].map((_, i) => {
                const status = getStatus(lab.id, i + 1);
                const color = status === 'occupied' ? 'bg-red-100 text-red-700' : status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700 cursor-pointer hover:ring-2';
                return (
                  <td key={i} className={`border p-2 text-center ${color}`} onClick={() => status === 'free' && onClick(lab, i + 1)}>
                    {status === 'free' && '+'}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex gap-4 mt-2 text-xs">
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-green-100 border"></div> 空闲</span>
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-red-100 border"></div> 占用</span>
        <span className="flex items-center gap-1"><div className="w-3 h-3 bg-yellow-100 border"></div> 待审批</span>
      </div>
    </div>
  );
};