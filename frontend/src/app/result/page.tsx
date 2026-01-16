'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import Link from 'next/link'
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
} from 'recharts'

// Sample formula data (in production, this would come from the API)
const sampleFormula = {
  name: 'Kyoto Morning Rain',
  description:
    'A contemplative blend capturing the essence of dawn in a Japanese garden, where petrichor meets ancient cypress.',
  topNotes: [
    { name: 'Yuzu', concentration: 8, sustainable: true },
    { name: 'Green Tea Accord', concentration: 5, sustainable: true },
    { name: 'Pink Pepper', concentration: 3, sustainable: false },
  ],
  middleNotes: [
    { name: 'Hinoki Wood', concentration: 15, sustainable: true },
    { name: 'Iris Pallida', concentration: 12, sustainable: true },
    { name: 'Shiso Leaf', concentration: 8, sustainable: true },
  ],
  baseNotes: [
    { name: 'Vetiver Haiti', concentration: 18, sustainable: true },
    { name: 'White Musk', concentration: 12, sustainable: true },
    { name: 'Ambergris Accord', concentration: 10, sustainable: false },
  ],
  metrics: {
    longevity: 85,
    projection: 65,
    uniqueness: 92,
    sustainability: 78,
    ifraCompliance: 100,
  },
}

// Scent pyramid visualization
function ScentPyramid({
  topNotes,
  middleNotes,
  baseNotes,
}: {
  topNotes: typeof sampleFormula.topNotes
  middleNotes: typeof sampleFormula.middleNotes
  baseNotes: typeof sampleFormula.baseNotes
}) {
  const [activeLayer, setActiveLayer] = useState<'top' | 'middle' | 'base' | null>(null)

  return (
    <div className="relative w-full max-w-md mx-auto">
      <svg viewBox="0 0 300 260" className="w-full h-auto">
        {/* Definitions */}
        <defs>
          <linearGradient id="pyramidGoldGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="rgba(232, 213, 163, 0.2)" />
            <stop offset="100%" stopColor="rgba(139, 115, 64, 0.1)" />
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        {/* Base layer */}
        <motion.g
          className="cursor-pointer"
          onMouseEnter={() => setActiveLayer('base')}
          onMouseLeave={() => setActiveLayer(null)}
          whileHover={{ scale: 1.02 }}
        >
          <motion.path
            d="M20 180 L280 180 L240 250 L60 250 Z"
            fill={activeLayer === 'base' ? 'rgba(201, 169, 98, 0.3)' : 'rgba(45, 27, 78, 0.5)'}
            stroke="rgba(201, 169, 98, 0.4)"
            strokeWidth="1"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          />
          <text x="150" y="222" textAnchor="middle" fill="rgba(201, 169, 98, 0.8)" fontSize="12" className="font-body">
            BASE NOTES
          </text>
        </motion.g>

        {/* Middle layer */}
        <motion.g
          className="cursor-pointer"
          onMouseEnter={() => setActiveLayer('middle')}
          onMouseLeave={() => setActiveLayer(null)}
          whileHover={{ scale: 1.02 }}
        >
          <motion.path
            d="M50 100 L250 100 L280 180 L20 180 Z"
            fill={activeLayer === 'middle' ? 'rgba(201, 169, 98, 0.3)' : 'rgba(45, 27, 78, 0.4)'}
            stroke="rgba(201, 169, 98, 0.4)"
            strokeWidth="1"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          />
          <text x="150" y="145" textAnchor="middle" fill="rgba(201, 169, 98, 0.8)" fontSize="12" className="font-body">
            HEART NOTES
          </text>
        </motion.g>

        {/* Top layer */}
        <motion.g
          className="cursor-pointer"
          onMouseEnter={() => setActiveLayer('top')}
          onMouseLeave={() => setActiveLayer(null)}
          whileHover={{ scale: 1.02 }}
        >
          <motion.path
            d="M100 30 L200 30 L250 100 L50 100 Z"
            fill={activeLayer === 'top' ? 'rgba(201, 169, 98, 0.3)' : 'rgba(45, 27, 78, 0.3)'}
            stroke="rgba(201, 169, 98, 0.4)"
            strokeWidth="1"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          />
          <text x="150" y="70" textAnchor="middle" fill="rgba(201, 169, 98, 0.8)" fontSize="12" className="font-body">
            TOP NOTES
          </text>
        </motion.g>
      </svg>

      {/* Layer details popup */}
      <AnimatePresence>
        {activeLayer && (
          <motion.div
            className="absolute left-full top-1/2 -translate-y-1/2 ml-4 w-48 p-4 glass-card"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
          >
            <h4 className="text-aether-gold text-sm font-medium mb-2 capitalize">
              {activeLayer} Notes
            </h4>
            <ul className="space-y-1">
              {(activeLayer === 'top'
                ? topNotes
                : activeLayer === 'middle'
                ? middleNotes
                : baseNotes
              ).map((note, i) => (
                <li key={i} className="flex items-center justify-between text-sm">
                  <span className="text-aether-cream/80">{note.name}</span>
                  <span className="text-aether-cream/50">{note.concentration}%</span>
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

// Metrics radar chart
function MetricsChart({ metrics }: { metrics: typeof sampleFormula.metrics }) {
  const data = [
    { metric: 'Longevity', value: metrics.longevity },
    { metric: 'Projection', value: metrics.projection },
    { metric: 'Uniqueness', value: metrics.uniqueness },
    { metric: 'Sustainability', value: metrics.sustainability },
    { metric: 'Safety', value: metrics.ifraCompliance },
  ]

  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart data={data}>
          <PolarGrid stroke="rgba(201, 169, 98, 0.2)" />
          <PolarAngleAxis
            dataKey="metric"
            tick={{ fill: 'rgba(245, 240, 232, 0.6)', fontSize: 11 }}
          />
          <Radar
            name="Metrics"
            dataKey="value"
            stroke="#c9a962"
            fill="#c9a962"
            fillOpacity={0.3}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}

// Ingredient list
function IngredientList({
  ingredients,
  title,
}: {
  ingredients: typeof sampleFormula.topNotes
  title: string
}) {
  return (
    <div className="mb-6">
      <h4 className="text-aether-gold text-sm font-medium mb-3">{title}</h4>
      <div className="space-y-2">
        {ingredients.map((ingredient, i) => (
          <motion.div
            key={i}
            className="flex items-center justify-between p-3 rounded-lg bg-aether-void/30 border border-aether-purple/20"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <div className="flex items-center gap-3">
              <span className="text-aether-cream">{ingredient.name}</span>
              {ingredient.sustainable && (
                <span className="px-2 py-0.5 rounded-full bg-green-500/20 text-green-400 text-xs">
                  Sustainable
                </span>
              )}
            </div>
            <span className="text-aether-cream/50 font-mono text-sm">
              {ingredient.concentration}%
            </span>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

// Progress steps
function ProgressSteps({ currentStep }: { currentStep: number }) {
  const steps = ['Bio-Calibration', 'Scent Brief', 'Your Formula']

  return (
    <div className="flex items-center justify-center gap-4 mb-12">
      {steps.map((step, index) => (
        <div key={step} className="flex items-center">
          <motion.div
            className={`progress-step ${index < currentStep ? 'completed' : ''} ${
              index === currentStep ? 'active' : ''
            }`}
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: index * 0.1 }}
          >
            {index < currentStep ? (
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            ) : (
              <span className="text-sm font-medium">{index + 1}</span>
            )}
          </motion.div>
          {index < steps.length - 1 && (
            <div
              className={`w-16 md:w-24 h-0.5 mx-2 transition-colors duration-500 ${
                index < currentStep ? 'bg-aether-gold' : 'bg-aether-purple/50'
              }`}
            />
          )}
        </div>
      ))}
    </div>
  )
}

// Loading animation
function LoadingAnimation() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-6">
      <motion.div
        className="relative w-32 h-32"
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: 'linear' }}
      >
        {/* Orbital rings */}
        {[0, 1, 2].map((i) => (
          <motion.div
            key={i}
            className="absolute inset-0 rounded-full border border-aether-gold/30"
            style={{
              transform: `rotateX(${60 + i * 20}deg) rotateY(${i * 30}deg)`,
            }}
            animate={{
              rotateZ: [0, 360],
            }}
            transition={{
              duration: 4 + i,
              repeat: Infinity,
              ease: 'linear',
            }}
          />
        ))}

        {/* Center glow */}
        <motion.div
          className="absolute inset-8 rounded-full bg-aether-gold/20"
          animate={{ scale: [1, 1.2, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </motion.div>

      <motion.div
        className="mt-8 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <h2 className="font-display text-2xl text-aether-cream mb-2">
          Formulating Your Essence
        </h2>
        <p className="text-aether-cream/60 text-sm">
          Analyzing bio-data and synthesizing molecules...
        </p>
      </motion.div>

      {/* Progress messages */}
      <motion.div
        className="mt-6 space-y-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
      >
        {[
          'Retrieving physiological rules...',
          'Calculating molecular compatibility...',
          'Optimizing volatility curves...',
          'Applying sustainability filters...',
        ].map((msg, i) => (
          <motion.p
            key={i}
            className="text-aether-gold/60 text-sm text-center"
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: [0, 1, 0.5] }}
            transition={{ delay: 1.5 + i * 0.8, duration: 2 }}
          >
            {msg}
          </motion.p>
        ))}
      </motion.div>
    </div>
  )
}

export default function ResultPage() {
  const [isLoading, setIsLoading] = useState(true)
  const [formula, setFormula] = useState(sampleFormula)
  const [showExport, setShowExport] = useState(false)

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 4000)

    return () => clearTimeout(timer)
  }, [])

  const handleExport = () => {
    const calibration = localStorage.getItem('aether_calibration')
    const neuroBrief = localStorage.getItem('aether_neuro_brief')

    const exportData = {
      formula,
      calibration: calibration ? JSON.parse(calibration) : null,
      neuroBrief: neuroBrief ? JSON.parse(neuroBrief) : null,
      exportedAt: new Date().toISOString(),
    }

    const blob = new Blob([JSON.stringify(exportData, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `aether-formula-${formula.name.toLowerCase().replace(/\s+/g, '-')}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  if (isLoading) {
    return <LoadingAnimation />
  }

  return (
    <div className="min-h-screen py-8 px-6">
      {/* Header */}
      <motion.nav
        className="max-w-6xl mx-auto flex items-center justify-between mb-8"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Link href="/" className="font-display text-xl text-gold-gradient">
          AETHER
        </Link>
        <Link href="/" className="text-aether-cream/50 hover:text-aether-gold transition-colors text-sm">
          Start Over
        </Link>
      </motion.nav>

      <div className="max-w-6xl mx-auto">
        {/* Progress */}
        <ProgressSteps currentStep={2} />

        {/* Formula header */}
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <motion.p
            className="text-aether-gold uppercase tracking-[0.2em] text-sm mb-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.3 }}
          >
            Your Personalized Formula
          </motion.p>
          <motion.h1
            className="font-display text-4xl md:text-6xl text-gold-gradient mb-4"
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
          >
            {formula.name}
          </motion.h1>
          <motion.p
            className="text-aether-cream/70 max-w-2xl mx-auto"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            {formula.description}
          </motion.p>
        </motion.div>

        {/* Main content grid */}
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Scent pyramid */}
          <motion.div
            className="glass-card p-6 lg:col-span-1"
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
          >
            <h3 className="text-aether-cream font-display text-xl mb-6 text-center">
              Scent Architecture
            </h3>
            <ScentPyramid
              topNotes={formula.topNotes}
              middleNotes={formula.middleNotes}
              baseNotes={formula.baseNotes}
            />
            <p className="text-aether-cream/40 text-xs text-center mt-4">
              Hover over layers to see ingredients
            </p>
          </motion.div>

          {/* Metrics chart */}
          <motion.div
            className="glass-card p-6 lg:col-span-1"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-aether-cream font-display text-xl mb-6 text-center">
              Performance Metrics
            </h3>
            <MetricsChart metrics={formula.metrics} />

            {/* Metric details */}
            <div className="grid grid-cols-2 gap-3 mt-4">
              {Object.entries(formula.metrics).map(([key, value]) => (
                <div
                  key={key}
                  className="p-2 rounded-lg bg-aether-void/30 text-center"
                >
                  <p className="text-aether-gold font-mono text-lg">{value}%</p>
                  <p className="text-aether-cream/50 text-xs capitalize">
                    {key.replace(/([A-Z])/g, ' $1').trim()}
                  </p>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Ingredients list */}
          <motion.div
            className="glass-card p-6 lg:col-span-1"
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.7 }}
          >
            <h3 className="text-aether-cream font-display text-xl mb-6">
              Full Composition
            </h3>
            <div className="max-h-96 overflow-y-auto pr-2">
              <IngredientList ingredients={formula.topNotes} title="Top Notes" />
              <IngredientList ingredients={formula.middleNotes} title="Heart Notes" />
              <IngredientList ingredients={formula.baseNotes} title="Base Notes" />
            </div>
          </motion.div>
        </div>

        {/* Actions */}
        <motion.div
          className="mt-12 flex flex-col sm:flex-row gap-4 justify-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          <motion.button
            className="btn-glow"
            onClick={handleExport}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
              Export Formula
            </span>
          </motion.button>

          <motion.button
            className="btn-ghost"
            onClick={() => setShowExport(true)}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <span className="flex items-center gap-2">
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z"
                />
              </svg>
              Share Result
            </span>
          </motion.button>

          <Link href="/calibration">
            <motion.button
              className="btn-ghost"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Create Another
            </motion.button>
          </Link>
        </motion.div>

        {/* IFRA compliance badge */}
        <motion.div
          className="mt-12 flex justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
        >
          <div className="flex items-center gap-3 px-4 py-2 rounded-full bg-green-500/10 border border-green-500/30">
            <svg className="w-5 h-5 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            <span className="text-green-400 text-sm">IFRA 51st Amendment Compliant</span>
          </div>
        </motion.div>
      </div>

      {/* Footer */}
      <footer className="mt-16 py-8 border-t border-aether-purple/30">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-sm">
          <p className="text-aether-cream/40">
            L'Oreal Brandstorm 2026 Innovation Challenge
          </p>
          <p className="text-aether-cream/40">
            Powered by Physio-RAG AI Technology
          </p>
        </div>
      </footer>
    </div>
  )
}
