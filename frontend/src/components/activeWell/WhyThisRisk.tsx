import { CheckCircle2, Layers3 } from 'lucide-react'
import type { RiskReason } from '../../types/domain'
import { PanelHeader } from '../common/PanelHeader'
export function WhyThisRisk({ reasons }: { reasons: RiskReason[] }) { return <section className="panel why-risk"><PanelHeader title="Why This Risk?" detail="Synthetic evidence chain behind the Risk Ahead signal" /><div className="reason-list">{reasons.map((reason) => <article key={reason.label} className="reason-item"><span className={`reason-item__strength reason-item__strength--${reason.strength}`}><Layers3 aria-hidden="true" size={16} /></span><div><div><strong>{reason.label}</strong><span><CheckCircle2 aria-hidden="true" size={12} /> {reason.strength} match</span></div><p>{reason.detail}</p></div></article>)}</div></section> }
