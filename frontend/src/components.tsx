import { useEffect, useState, type ButtonHTMLAttributes, type ReactNode } from 'react';
import { Link, NavLink, useLocation, useNavigate } from 'react-router-dom';
import {
  Bell, BriefcaseBusiness, ChevronRight, CircleDollarSign, Compass, Home, Inbox, LayoutDashboard,
  LogOut, MessageCircle, Plus, Search, Settings, Sparkles, Users, WalletCards, X,
} from 'lucide-react';
import { useAuth } from './context';
import type { User, Work } from './types';

export function Logo() {
  return <Link to="/dashboard" className="logo"><span className="logo-mark">◒</span><span>loopline</span></Link>;
}

export function Avatar({ user, size = 'md' }: { user?: Partial<User> | null; size?: 'sm' | 'md' | 'lg' }) {
  const initials = user?.name?.split(' ').map((word) => word[0]).join('').slice(0, 2).toUpperCase() ?? 'LL';
  return <span className={`avatar avatar-${size}`} title={user?.name}>{initials}</span>;
}

export function Button({ children, variant = 'primary', className = '', ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: 'primary' | 'secondary' | 'ghost' | 'danger' }) {
  return <button className={`button button-${variant} ${className}`} {...props}>{children}</button>;
}

export function Card({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <section className={`card ${className}`}>{children}</section>;
}

export function Badge({ children, tone = 'neutral' }: { children: ReactNode; tone?: 'neutral' | 'green' | 'orange' | 'purple' | 'red' }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export function EmptyState({ icon, title, body, action }: { icon?: ReactNode; title: string; body: string; action?: ReactNode }) {
  return <div className="empty-state">{icon ?? <Sparkles size={22} />}<h3>{title}</h3><p>{body}</p>{action}</div>;
}

export function Loading() {
  return <div className="loading"><span className="spinner" />Loading your workspace…</div>;
}

const navItems = [
  { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
  { to: '/feed', label: 'Feed', icon: Home },
  { to: '/search', label: 'Discover people', icon: Users },
  { to: '/works/active', label: 'My work', icon: BriefcaseBusiness },
  { to: '/requests', label: 'Requests', icon: Inbox },
  { to: '/chats', label: 'Messages', icon: MessageCircle },
];

export function AppShell({ children }: { children: ReactNode }) {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-top"><Logo /><button className="icon-button mobile-close" onClick={() => setMobileOpen(false)} aria-label="Close menu"><X size={19} /></button></div>
        <div className="sidebar-profile"><Avatar user={user} /><div><strong>{user?.name}</strong><span>@{user?.username}</span></div><Link to={`/profile/${user?.username}`} aria-label="View profile"><ChevronRight size={16} /></Link></div>
        <nav className="main-nav">
          <p className="nav-label">Workspace</p>
          {navItems.map(({ to, label, icon: Icon }) => <NavLink key={to} to={to} onClick={() => setMobileOpen(false)} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}><Icon size={18} /><span>{label}</span>{label === 'Requests' && <span className="nav-dot" />}</NavLink>)}
          <p className="nav-label nav-label-space">More</p>
          <NavLink to="/transactions" className="nav-link"><WalletCards size={18} /><span>Demo wallet</span></NavLink>
          <NavLink to="/notifications" className="nav-link"><Bell size={18} /><span>Notifications</span></NavLink>
          <NavLink to="/ai-assistant" className="nav-link"><Sparkles size={18} /><span>AI assistant</span><span className="ai-chip">AI</span></NavLink>
          <NavLink to="/settings" className="nav-link"><Settings size={18} /><span>Settings</span></NavLink>
        </nav>
        <div className="sidebar-bottom"><button className="nav-link logout" onClick={() => { signOut(); navigate('/login'); }}><LogOut size={18} /><span>Sign out</span></button><div className="demo-note"><CircleDollarSign size={16} /><span>Everything here is<br /><b>demo / simulated</b></span></div></div>
      </aside>
      <main className="main-area">
        <header className="topbar"><button className="icon-button mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open menu"><Compass size={20} /></button><div className="topbar-search"><Search size={17} /><input placeholder="Search people, skills, opportunities…" onKeyDown={(event) => { if (event.key === 'Enter') navigate(`/search?q=${encodeURIComponent(event.currentTarget.value)}`); }} /></div><div className="topbar-actions"><Link to="/notifications" className="icon-button"><Bell size={19} /><span className="notification-pip" /></Link><Link to="/create" className="button button-primary button-small"><Plus size={16} />Create</Link><Link to={`/profile/${user?.username}`}><Avatar user={user} size="sm" /></Link></div></header>
        <div className="page-wrap" key={location.pathname}><div className="page-transition">{children}</div></div>
      </main>
      <nav className="bottom-nav">{navItems.slice(0, 5).map(({ to, label, icon: Icon }) => <NavLink key={to} to={to}><Icon size={18} /><span>{label === 'Discover people' ? 'People' : label}</span></NavLink>)}</nav>
    </div>
  );
}

export function PageHeader({ eyebrow, title, description, action }: { eyebrow?: string; title: string; description?: string; action?: ReactNode }) {
  return <div className="page-header"><div>{eyebrow && <p className="eyebrow">{eyebrow}</p>}<h1>{title}</h1>{description && <p className="page-description">{description}</p>}</div>{action}</div>;
}

export function Countdown({ work }: { work: Work }) {
  const [remaining, setRemaining] = useState('');
  useEffect(() => {
    const tick = () => {
      if (!work.due_at) return setRemaining('No deadline');
      const difference = new Date(work.due_at).getTime() - Date.now();
      if (difference <= 0) return setRemaining('Overdue');
      const totalSeconds = Math.floor(difference / 1000);
      const days = Math.floor(totalSeconds / 86400);
      const hours = Math.floor((totalSeconds % 86400) / 3600);
      const minutes = Math.floor((totalSeconds % 3600) / 60);
      setRemaining(`${days}d ${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m`);
    };
    tick();
    const timer = window.setInterval(tick, 60000);
    return () => window.clearInterval(timer);
  }, [work.due_at]);
  return <span className={remaining === 'Overdue' || work.is_overdue ? 'countdown overdue' : 'countdown'}>{remaining}</span>;
}

export function WorkCard({ work, onAction }: { work: Work; onAction?: () => void }) {
  const canApply = work.status === 'OPEN';
  return <Card className="work-card"><div className="work-card-top"><div className="work-type"><span className="mini-icon"><BriefcaseBusiness size={15} /></span><span>{work.work_mode} · {work.location}</span></div><Badge tone={work.status === 'OVERDUE' ? 'red' : work.status === 'OPEN' ? 'purple' : 'green'}>{work.status.replace('_', ' ')}</Badge></div><Link to={`/works/${work.id}`}><h3>{work.title}</h3></Link><p>{work.description}</p><div className="skill-row"><span className="skill-pill">Product</span><span className="skill-pill">Collaboration</span><span className="skill-pill">↗ view details</span></div><div className="work-card-meta"><div><span className="meta-label">Demo compensation</span><strong>₹{work.budget.toLocaleString('en-IN')}</strong></div>{work.due_at ? <div><span className="meta-label">Deadline</span><Countdown work={work} /></div> : <div><span className="meta-label">Complete within</span><strong>{work.deadline_duration_days} days</strong></div>}</div>{onAction && <Button variant={canApply ? 'primary' : 'secondary'} className="full-button" onClick={onAction}>{canApply ? 'Apply to opportunity' : 'Open work details'}<ChevronRight size={16} /></Button>}</Card>;
}