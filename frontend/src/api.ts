const API_PREFIX = '/api/v1'

/** Builds the URL of an application API resource, e.g. apiPath('/health'). */
export function apiPath(resource: string): string {
  return resource.startsWith('/') ? `${API_PREFIX}${resource}` : `${API_PREFIX}/${resource}`
}
