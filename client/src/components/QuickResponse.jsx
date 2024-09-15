import { motion } from 'framer-motion'
import { Check, ChevronRight } from 'lucide-react'
import React, { useEffect } from 'react'

const QuickResponse = ({ text, onClick }) => {
  const [isOpen, setIsOpen] = React.useState(false)

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => {
        setIsOpen(false)
      }, 2000)
    }
  }, [isOpen])

  return (
    <motion.button
      className={`rounded-full ${
        isOpen ? 'bg-[#4A8FF7]' : 'bg-[#EF8E47]'
      } px-4 py-2 font-semibold text-white`}
      animate={{
        rotate: isOpen ? 180 : 0,
      }}
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => {
        setIsOpen(!isOpen);
        onClick();
      }}
    >
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
      >
        {isOpen ? (
          <span className="flex rotate-180 items-center gap-1 text-sm font-medium">
            {text} <Check size={16} />
          </span>
        ) : (
          <span className="flex items-center gap-1 text-sm font-medium">
            {text} <ChevronRight size={16} />
          </span>
        )}
      </motion.span>
    </motion.button>
  )
}

export default QuickResponse