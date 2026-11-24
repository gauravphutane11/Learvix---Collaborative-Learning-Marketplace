import { Link, useLocation } from "react-router-dom";
import { useState } from "react";
import {
  Home,
  Users,
  TrendingUp,
  Bell,
  User,
  LogOut,
  Zap,
  Menu,
  X,
  Sparkles
} from "lucide-react";

const NAV_LINKS = [
  { to: "/",             label: "Home",          icon: Home        },
  { to: "/skillproof",   label: "SkillProof",    icon: Sparkles    },
  { to: "/matching",     label: "Matching",      icon: Users       },
  { to: "/progress",     label: "Progress",      icon: TrendingUp  },
  { to: "/notifications",label: "Notifications", icon: Bell        },
  { to: "/profile",      label: "Profile",       icon: User        },
];

export default function Navbar({ currentUser, onLogout, unreadNotifications }) {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);
  const isActive = (path) => path === "/" ? location.pathname === "/" : location.pathname.startsWith(path);
  const initials = currentUser?.name ? currentUser.name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase() : "LX";

  return (
    <header className="lx-header">
      <nav className="lx-nav">
        <Link to="/" className="lx-brand" aria-label="Learvix home">
          <span className="lx-brand-mark"><Sparkles size={19} /></span>
          <span>Learvix<span className="lx-brand-period">.</span></span>
        </Link>
        <div className="lx-nav-links">
          {NAV_LINKS.map(({ to, label, icon: Icon }) => (
            <Link key={to} to={to} onClick={() => setMobileOpen(false)} className={`lx-nav-link ${isActive(to) ? "is-active" : ""}`}>
              <Icon size={17} /><span>{label}</span>
              {label === "Notifications" && unreadNotifications > 0 && <span className="lx-nav-count">{unreadNotifications > 9 ? "9+" : unreadNotifications}</span>}
            </Link>
          ))}
        </div>
        <div className="lx-nav-user">
          <span className="lx-user-avatar">{currentUser?.profileImage ? <img src={currentUser.profileImage} alt=""/> : (currentUser?.avatar || initials)}</span>
          <span className="lx-user-meta"><strong>{currentUser?.name || "Learner"}</strong><small>Learning member</small></span>
          <button className="lx-logout" onClick={onLogout}><LogOut size={16}/><span>Log out</span></button>
        </div>
        <button className="lx-menu-toggle" onClick={() => setMobileOpen((v) => !v)} aria-label="Toggle navigation">{mobileOpen ? <X/> : <Menu/>}</button>
      </nav>
      {mobileOpen && <div className="lx-mobile-menu">
        {NAV_LINKS.map(({to,label,icon:Icon}) => <Link key={to} to={to} onClick={() => setMobileOpen(false)} className={`lx-mobile-link ${isActive(to) ? "is-active" : ""}`}><Icon size={17}/>{label}{label === "Notifications" && unreadNotifications > 0 ? <span className="lx-nav-count">{unreadNotifications}</span> : null}</Link>)}
        <button className="lx-mobile-logout" onClick={onLogout}><LogOut size={16}/> Log out</button>
      </div>}
    </header>
  );
}
