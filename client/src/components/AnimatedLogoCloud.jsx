const logos = [
    {
      name: 'groq',
      url: 'groq.png',
    },
    {
      name: 'Shopify',
      url: 'Shopify.svg',
    },
    {
      name: 'Reddit',
      url: 'reddit.png',
    },
    {
      name: 'Google',
      url: 'google.png',
    },
  
    {
      name: 'Meta Llama',
      url: 'meta.png',
    },
    {
      name: 'GoDaddy',
      url: 'godaddy.png',
    },
    {
      name: 'Stackoverflow',
      url: 'https://res.cloudinary.com/dfhp33ufc/image/upload/v1715276558/logos/ts1j4mkooxqmscgptafa.svg',
    },
  ]
  
  const AnimatedLogoCloud = () => {
    return (
      <div className="w-full py-4">
        <div className="mx-auto w-full px-4 md:px-8">
          <div
            className="group relative flex gap-6 overflow-hidden p-2"
            style={{
              maskImage:
                'linear-gradient(to left, transparent 0%, black 20%, black 80%, transparent 95%)',
            }}
          >
            {Array(5)
              .fill(null)
              .map((_, index) => (
                <div
                  key={index}
                  className="flex shrink-0 animate-logo-cloud flex-row justify-around gap-6"
                >
                  {logos.map((logo, key) => (
                    <img
                      key={key}
                      src={logo.url}
                      className="h-10 min-w-8 w-auto px-2 brightness-0 dark:invert"
                      alt={`${logo.name}`}
                      style={{ filter: 'invert(0.29) sepia(1) saturate(5) hue-rotate(180deg)' }}
                    />
                  ))}
                </div>
              ))}
          </div>
        </div>
      </div>
    )
  }
  
  export default AnimatedLogoCloud