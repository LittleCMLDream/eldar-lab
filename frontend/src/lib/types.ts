export interface Lab { id: number; name: string; building: string; room_number: string; }
export interface Booking { id: number; lab_id: number; week: number; day: number; start: number; end: number; status: 'free' | 'occupied' | 'pending'; course_name?: string; }
export interface BookingForm { course: string; class: string; reason: string; content: string; }