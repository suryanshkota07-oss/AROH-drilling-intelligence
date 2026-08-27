import type { ReactNode } from 'react'
export function PanelHeader({ title, detail, action }: { title: string; detail?: string; action?: ReactNode }) { return <div className="panel-header"><div><h2>{title}</h2>{detail ? <p>{detail}</p> : null}</div>{action}</div> }
