import { Wifi } from 'lucide-react'
export function Header() { return <header className="app-header"><div><p className="eyebrow">OPERATIONS OVERVIEW</p><h1>Command Center</h1></div><div className="header-actions"><span className="system-status"><Wifi aria-hidden="true" size={15} />System online</span><span className="user-avatar" aria-label="Demo user">DE</span></div></header> }
