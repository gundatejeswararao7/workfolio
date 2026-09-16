import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { api } from './api';
import type { User } from './types';

interface AuthContextValue {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    if (!localStorage.getItem('loopline_token')) return;
    try {
      setUser(await api.get<User>('/users/me'));
    } catch {
      localStorage.removeItem('loopline_token');
      setUser(null);
    }
  };

  useEffect(() => {
    refreshUser().finally(() => setLoading(false));
  }, []);

  const signIn = async (email: string, password: string) => {
    const result = await api.post<{ token: string }>('/auth/login', { email, password });
    localStorage.setItem('loopline_token', result.token);
    await refreshUser();
  };

  const signOut = () => {
    localStorage.removeItem('loopline_token');
    setUser(null);
  };

  return <AuthContext.Provider value={{ user, loading, signIn, signOut, refreshUser }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const value = useContext(AuthContext);
  if (!value) throw new Error('useAuth must be used inside AuthProvider');
  return value;
}