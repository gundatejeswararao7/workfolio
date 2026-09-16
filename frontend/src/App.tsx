import { Navigate, Route, Routes } from 'react-router-dom';
import type { ReactNode } from 'react';
import { AppShell, Loading } from './components';
import { AuthProvider, useAuth } from './context';
import {
  ActiveWorksPage, AIPage, ChatsPage, CreatePage, DashboardPage, FeedPage, ForgotPasswordPage,
  LoginPage, NotificationsPage, ProfilePage, RegisterPage, RequestsPage, SearchPage, SettingsPage,
  TransactionsPage, WorkDetailPage,
} from './pages';

function Protected({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  return user ? <AppShell>{children}</AppShell> : <Navigate to="/login" replace />;
}

function PublicOnly({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  if (loading) return <Loading />;
  return user ? <Navigate to="/dashboard" replace /> : <>{children}</>;
}

export default function App() {
  return <AuthProvider><Routes>
    <Route path="/login" element={<PublicOnly><LoginPage /></PublicOnly>} />
    <Route path="/register" element={<PublicOnly><RegisterPage /></PublicOnly>} />
    <Route path="/forgot-password" element={<PublicOnly><ForgotPasswordPage /></PublicOnly>} />
    <Route path="/dashboard" element={<Protected><DashboardPage /></Protected>} />
    <Route path="/feed" element={<Protected><FeedPage /></Protected>} />
    <Route path="/search" element={<Protected><SearchPage /></Protected>} />
    <Route path="/create" element={<Protected><CreatePage /></Protected>} />
    <Route path="/works/active" element={<Protected><ActiveWorksPage /></Protected>} />
    <Route path="/works/completed" element={<Protected><ActiveWorksPage completed /></Protected>} />
    <Route path="/works/:id" element={<Protected><WorkDetailPage /></Protected>} />
    <Route path="/requests" element={<Protected><RequestsPage /></Protected>} />
    <Route path="/notifications" element={<Protected><NotificationsPage /></Protected>} />
    <Route path="/transactions" element={<Protected><TransactionsPage /></Protected>} />
    <Route path="/ai-assistant" element={<Protected><AIPage /></Protected>} />
    <Route path="/chats" element={<Protected><ChatsPage /></Protected>} />
    <Route path="/profile/:username" element={<Protected><ProfilePage /></Protected>} />
    <Route path="/settings" element={<Protected><SettingsPage /></Protected>} />
    <Route path="*" element={<Navigate to="/dashboard" replace />} />
  </Routes></AuthProvider>;
}