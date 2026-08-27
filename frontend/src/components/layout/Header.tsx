import { Wifi } from 'lucide-react'
import { useLocation } from 'react-router-dom'
const pageTitles: Record<string, string> = { '/command-center': 'Command Center', '/active-well': 'Active Well' }
export function Header() { const { pathname } = useLocation(); return <header className="app-header"><div><p className="eyebrow">OPERATIONS OVERVIEW</p><h1>{pageTitles[pathname] ?? 'AROH'}</h1></div><div className="header-actions"><span className="system-status"><Wifi aria-hidden="true" size={15} />System online</span><span className="user-avatar" aria-label="Demo user">DE</span></div></header> }
