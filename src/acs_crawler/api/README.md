# Frontend Architecture Documentation

## Overview

The ACS Crawler frontend follows modern web development best practices with clear separation of concerns, modular architecture, and maintainable code structure.

## Architecture Principles

### 1. **Separation of Concerns (SoC)**
Each component has a single, well-defined responsibility:
- **HTML**: Structure and content (templates)
- **CSS**: Presentation and styling (static/css)
- **JavaScript**: Behavior and logic (static/js)
- **Data**: API responses (JSON via REST API)

### 2. **Modular Design**
JavaScript is organized into focused modules:
- `api.js`: API communication layer
- `charts.js`: Chart rendering and visualization
- `ui.js`: UI utilities and helpers
- `dashboard.js`: Page-specific controller

### 3. **Progressive Enhancement**
- Core functionality works without JavaScript
- Enhanced features added via JS
- Graceful degradation for older browsers

### 4. **Single Responsibility Principle**
Each module/function does one thing well:
- API calls don't handle UI
- Charts don't fetch data
- UI utilities don't contain business logic

## Project Structure

```
src/acs_crawler/api/
├── static/                      # Static assets
│   ├── css/
│   │   └── dashboard.css       # Custom styles
│   └── js/
│       ├── api.js              # API service layer
│       ├── charts.js           # Chart rendering
│       ├── ui.js               # UI utilities
│       └── dashboard.js        # Dashboard controller
├── templates/                   # Jinja2 templates
│   ├── base.html               # Base layout
│   ├── index.html              # Dashboard page
│   ├── jobs.html               # Jobs listing
│   ├── papers.html             # Papers listing
│   └── paper_detail.html       # Paper details
└── main.py                      # FastAPI application
```

## Module Architecture

### API Service Layer (`api.js`)

**Purpose**: Centralized API communication

**Responsibilities**:
- Make HTTP requests to backend
- Handle errors consistently
- Return parsed JSON data
- Provide type-safe interfaces

**Key Methods**:
```javascript
API.getJournals()        // Fetch journals list
API.getStatistics()      // Fetch statistics
API.createJob(url)       // Create crawl job
API.getJobs()            // Get all jobs
API.getPapers()          // Get all papers
```

**Design Patterns**:
- **Singleton**: Single API object
- **Promise-based**: Async/await for clean code
- **Error handling**: Try-catch with logging

**Benefits**:
- ✅ Centralized error handling
- ✅ Easy to mock for testing
- ✅ Single source of truth for endpoints
- ✅ Reusable across pages

### Charts Module (`charts.js`)

**Purpose**: Chart creation and rendering

**Responsibilities**:
- Create Chart.js visualizations
- Manage chart instances
- Apply consistent theming
- Handle chart lifecycle

**Key Methods**:
```javascript
Charts.createJournalChart()         // Doughnut chart
Charts.createAuthorsChart()         // Bar chart
Charts.createTimelineChart()        // Line chart
Charts.createPublicationYearsChart() // Bar chart
Charts.renderAll(stats)             // Render all
Charts.destroyAll()                 // Cleanup
```

**Design Patterns**:
- **Factory**: Create charts with consistent config
- **Registry**: Track chart instances
- **Template Method**: Reusable chart options

**Benefits**:
- ✅ Consistent chart styling
- ✅ Easy to add new chart types
- ✅ Memory leak prevention (destroy old charts)
- ✅ Responsive by default

### UI Utilities (`ui.js`)

**Purpose**: Reusable UI helper functions

**Responsibilities**:
- Show/hide alerts
- Button loading states
- Date formatting
- Form validation
- DOM manipulation

**Key Methods**:
```javascript
UI.showAlert()           // Display alert
UI.hideAlert()           // Hide alert
UI.setButtonLoading()    // Button state
UI.populateSelect()      // Fill dropdown
UI.formatDate()          // Format dates
UI.debounce()            // Debounce inputs
UI.isValidUrl()          // Validate URL
```

**Design Patterns**:
- **Utility Object**: Stateless helper functions
- **Decorator**: Enhance elements with behavior
- **Strategy**: Different formatting strategies

**Benefits**:
- ✅ DRY (Don't Repeat Yourself)
- ✅ Consistent UX across pages
- ✅ Easy to test
- ✅ Reusable across projects

### Dashboard Controller (`dashboard.js`)

**Purpose**: Orchestrate dashboard page

**Responsibilities**:
- Initialize page components
- Coordinate modules
- Handle user interactions
- Manage page state

**Key Methods**:
```javascript
Dashboard.init()              // Initialize page
Dashboard.loadJournals()      // Load dropdown
Dashboard.loadStatistics()    // Load charts
Dashboard.handleJobSubmit()   // Submit form
Dashboard.refreshStatistics() // Update charts
```

**Design Patterns**:
- **Controller**: MVC pattern controller
- **Mediator**: Coordinates modules
- **Observer**: Event-driven architecture

**Benefits**:
- ✅ Single entry point per page
- ✅ Clear initialization flow
- ✅ Testable business logic
- ✅ Easy to extend

## Data Flow

```
┌─────────────┐
│   User      │
│  Actions    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Dashboard  │◄──── Page Controller
│  Controller │
└──────┬──────┘
       │
       ├──────────┐
       │          │
       ▼          ▼
┌──────────┐ ┌──────────┐
│   API    │ │   UI     │
│  Module  │ │  Module  │
└─────┬────┘ └─────┬────┘
      │            │
      ▼            ▼
┌──────────┐ ┌──────────┐
│ Backend  │ │   DOM    │
│   API    │ │ Elements │
└─────┬────┘ └──────────┘
      │
      ▼
┌──────────┐
│  Charts  │◄──── Visualization Layer
│  Module  │
└──────────┘
```

## Frontend Design Principles Applied

### 1. **DRY (Don't Repeat Yourself)**
- Reusable UI functions in `ui.js`
- Consistent chart creation in `charts.js`
- Shared API logic in `api.js`

### 2. **KISS (Keep It Simple, Stupid)**
- Clear function names
- Single purpose per module
- Minimal dependencies

### 3. **YAGNI (You Aren't Gonna Need It)**
- No premature optimization
- Features added as needed
- Simple solutions first

### 4. **Loose Coupling**
- Modules don't depend on each other directly
- Communication through clean interfaces
- Easy to replace modules

### 5. **High Cohesion**
- Related functions grouped together
- Each module has clear purpose
- Minimal cross-module dependencies

### 6. **Consistent Naming**
- Verbs for actions: `loadJournals()`, `createChart()`
- Nouns for data: `journalData`, `statsResponse`
- Descriptive names: `handleJobSubmit()` not `submit()`

### 7. **Error Handling**
- Try-catch blocks everywhere
- Console logging for debugging
- User-friendly error messages
- Graceful fallbacks

### 8. **Performance**
- Lazy loading of charts
- Debounced input handlers
- Efficient DOM updates
- Chart instance cleanup

### 9. **Accessibility**
- Semantic HTML
- ARIA labels on charts
- Keyboard navigation
- Screen reader support

### 10. **Responsive Design**
- Mobile-first CSS
- Flexible grid layouts
- Touch-friendly interactions
- Adaptive chart sizing

## CSS Architecture

### Principles
- **BEM-like naming**: `.chart-card__header`
- **Component-based**: Each component in own section
- **Mobile-first**: Base styles for mobile, desktop overrides
- **CSS Variables**: Consistent colors and spacing
- **No !important**: Proper specificity

## Best Practices Implemented

### JavaScript

✅ **Modular Code**: Each file has single responsibility
✅ **Async/Await**: Modern async handling
✅ **Error Handling**: Try-catch everywhere
✅ **JSDoc Comments**: Clear documentation
✅ **Const/Let**: No var usage
✅ **Arrow Functions**: Concise syntax
✅ **Template Literals**: Clean string formatting
✅ **Destructuring**: Clean parameter handling

### HTML

✅ **Semantic Tags**: Proper element usage
✅ **Accessibility**: ARIA labels, alt text
✅ **SEO**: Meta tags, structured data
✅ **Template Inheritance**: DRY templates
✅ **Clean Structure**: Logical nesting

### CSS

✅ **Mobile-First**: Responsive by default
✅ **Flexbox/Grid**: Modern layouts
✅ **Animations**: Smooth transitions
✅ **Variables**: Consistent theming
✅ **Performance**: GPU acceleration

## Testing Strategy

### Unit Testing
```javascript
// Test API module
test('API.getJournals returns data', async () => {
    const data = await API.getJournals();
    expect(data.journals).toBeDefined();
});

// Test UI module
test('UI.isValidUrl validates URLs', () => {
    expect(UI.isValidUrl('https://example.com')).toBe(true);
    expect(UI.isValidUrl('not-a-url')).toBe(false);
});
```

### Integration Testing
- Test module interactions
- Test API + UI flow
- Test Chart rendering

### E2E Testing
- Test complete user workflows
- Test form submissions
- Test chart interactions

## Performance Optimization

### Implemented
- ✅ Debounced input handlers
- ✅ Lazy chart initialization
- ✅ Efficient DOM queries
- ✅ Chart instance reuse
- ✅ Minimal reflows

### Future Optimizations
- 🔜 Code splitting
- 🔜 Service Workers
- 🔜 Image lazy loading
- 🔜 CDN for static assets

## Security Considerations

### Implemented
- ✅ Input validation
- ✅ XSS prevention (template escaping)
- ✅ CSRF tokens (FastAPI)
- ✅ URL validation
- ✅ No inline scripts

### Best Practices
- Never use `eval()`
- Sanitize user input
- Use HTTPS in production
- Content Security Policy
- Regular dependency updates

## Browser Support

### Target Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Polyfills Needed
- None (modern browsers only)

## Deployment Checklist

- [ ] Minify JavaScript
- [ ] Minify CSS
- [ ] Optimize images
- [ ] Enable gzip compression
- [ ] Set cache headers
- [ ] Enable CDN
- [ ] Security headers
- [ ] HTTPS enabled

## Maintenance

### Adding New Features
1. Add API method to `api.js`
2. Add UI helper to `ui.js` if needed
3. Add chart type to `charts.js` if needed
4. Update controller in `dashboard.js`
5. Update template HTML
6. Update CSS styles

### Debugging
- Check browser console for errors
- Use Chrome DevTools Network tab
- Inspect API responses
- Check chart instances
- Validate HTML structure

## Documentation Links

- **Chart.js**: https://www.chartjs.org/docs/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **FastAPI**: https://fastapi.tiangolo.com/
- **Jinja2**: https://jinja.palletsprojects.com/

## Conclusion

This architecture provides:
- ✅ **Maintainability**: Easy to update and extend
- ✅ **Scalability**: Add features without breaking existing code
- ✅ **Testability**: Modules can be tested independently
- ✅ **Performance**: Optimized for speed
- ✅ **Accessibility**: Works for all users
- ✅ **Professionalism**: Production-ready code quality

The separation of concerns ensures that changes to one aspect (styling, data fetching, visualization) don't affect others, making the codebase more maintainable and easier to understand.
