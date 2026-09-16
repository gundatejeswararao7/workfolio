export interface User {
  id: number;
  name: string;
  username: string;
  email: string;
  bio: string;
  location: string;
  availability: string;
  profile_image: string;
  skills: string[];
  rating: number;
  completed_works: number;
}

export interface Post {
  id: number;
  content: string;
  media_url: string;
  media_type: string;
  likes_count: number;
  comments_count: number;
  created_at: string;
  author: User;
}

export interface Work {
  id: number;
  requester_id: number;
  assignee_id: number | null;
  title: string;
  description: string;
  status: string;
  budget: number;
  deadline_duration_days: number;
  application_deadline: string | null;
  accepted_at: string | null;
  due_at: string | null;
  submitted_at: string | null;
  completed_at: string | null;
  is_overdue: boolean;
  was_submitted_late: boolean;
  location: string;
  work_mode: string;
  progress: number;
  requester_name: string;
  assignee_name: string;
}

export interface Notification {
  id: number;
  type: string;
  title: string;
  body: string;
  is_read: boolean;
  created_at: string;
}

export interface Transaction {
  id: string;
  amount: number;
  type: string;
  status: string;
  created_at: string;
  direction: 'received' | 'sent';
}

export interface ChatSummary {
  id: number;
  other_user: { name: string; username: string } | null;
  last_message: string;
  unread_count: number;
}