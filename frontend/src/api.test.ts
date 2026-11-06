import { describe, expect, it } from 'vitest'
import { apiPath } from './api'

describe('apiPath', () => {
  it('prefixes a resource with the API version', () => {
    expect(apiPath('/health')).toBe('/api/v1/health')
  })

  it('adds the slash when the resource has none', () => {
    expect(apiPath('health')).toBe('/api/v1/health')
  })
})
