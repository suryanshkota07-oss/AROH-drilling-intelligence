import { ArrowDown, ArrowUp, Minus } from 'lucide-react'
import type { DrillingParameter } from '../../types/domain'
import { PanelHeader } from '../common/PanelHeader'
const trendIcon = { rising: ArrowUp, stable: Minus, falling: ArrowDown }
export function DrillingParameters({ parameters }: { parameters: DrillingParameter[] }) { return <section className="panel drilling-parameters"><PanelHeader title="Current Drilling Parameters" detail="Latest values from the synthetic telemetry stream" /><div className="parameter-grid">{parameters.map((parameter) => { const TrendIcon = trendIcon[parameter.trend]; return <article key={parameter.label} className="parameter-card"><div><span>{parameter.label}</span><i className={`parameter-trend parameter-trend--${parameter.trend}`}><TrendIcon aria-hidden="true" size={14} /></i></div><strong>{parameter.value.toLocaleString()} <small>{parameter.unit}</small></strong><p>{parameter.detail}</p></article> })}</div></section> }
