# Frontend Refactoring Guide

## Overview

The frontend has been completely refactored to follow modern React best practices with a focus on:
- **Composability**: Reusable hooks and components
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new features
- **Type Safety**: Full TypeScript coverage
- **User Experience**: Toast notifications and error handling

## Architecture

### Custom Hooks (`/src/hooks/`)

#### `useFileConverter`
**Purpose**: Manages the complete file conversion workflow including upload, polling, and status tracking.

**Features**:
- Generic file upload with custom upload function
- Automatic job status polling
- Cleanup on unmount
- Error handling
- State management for file, jobId, status, uploading, error

**Usage**:
```typescript
const converter = useFileConverter({
  uploadFn: async (file: File) => {
    return await bandMusicAPI.uploadOMRFile(file);
  },
  getStatusFn: async (jobId: string) => {
    return await bandMusicAPI.getJobStatus(jobId);
  },
  pollInterval: 2000, // optional, defaults to 2000ms
});
```

#### `useFileUpload`
**Purpose**: Handles file selection, validation, and size formatting.

**Features**:
- File type validation via `accept` prop
- File size validation with customizable max size
- File size formatting utility
- Error management

**Usage**:
```typescript
const fileUpload = useFileUpload({
  accept: '.pdf,.png,.jpg',
  maxSize: 100 * 1024 * 1024, // 100MB
  onFileSelect: (file) => console.log('File selected:', file),
});
```

### Context Providers (`/src/contexts/`)

#### `ToastContext`
**Purpose**: Global toast notification system.

**Features**:
- Show toast messages with type (success, error, info, warning)
- Auto-dismiss after configurable duration
- Manual dismiss option
- Queue multiple toasts

**Usage**:
```typescript
const { showToast, removeToast } = useToast();

showToast('File uploaded successfully!', 'success', 5000);
showToast('An error occurred', 'error');
```

### Reusable Components (`/src/components/common/`)

#### `FileUpload`
File input component with validation feedback.

**Props**:
- `accept`: File type filter (string)
- `onChange`: File change handler
- `disabled`: Disable state (boolean)
- `label`: Input label (string)
- `file`: Selected file object (optional)
- `error`: Error message (optional)
- `formatFileSize`: Size formatting function (optional)

#### `ProgressBar`
Animated progress bar with percentage display.

**Props**:
- `progress`: Progress value 0-100 (number)
- `label`: Progress label (optional string)
- `color`: Color theme - 'blue', 'purple', 'green' (optional)

#### `Alert`
Alert/notification component with different styles.

**Props**:
- `type`: Alert type - 'error', 'success', 'info', 'warning'
- `title`: Alert title (optional string)
- `message`: Alert message (string)
- `onClose`: Close handler (optional function)

#### `StatusDisplay`
Job status display with progress bar and action buttons.

**Props**:
- `status`: JobStatus object
- `color`: Theme color - 'blue', 'purple', 'green'
- `onDownload`: Download handler (optional function)
- `onReset`: Reset handler (optional function)
- `downloadButtonText`: Download button label (optional string)

#### `PipelineInfo`
Display pipeline steps information.

**Props**:
- `steps`: Array of `{ title: string, description: string }`

#### `ToastContainer`
Renders all active toast notifications.

**Usage**: Place once at app root level.

## Component Structure

### Converter Components Pattern

Both `OMRConverter` and `AMTConverter` follow the same refactored pattern:

```typescript
const ConverterComponent: React.FC = () => {
  // 1. Get toast context
  const { showToast } = useToast();
  
  // 2. Initialize file upload hook
  const fileUpload = useFileUpload({
    accept: '.pdf,.png,.jpg',
    maxSize: 100 * 1024 * 1024,
  });

  // 3. Initialize converter hook
  const converter = useFileConverter({
    uploadFn: async (file) => await api.uploadFile(file),
    getStatusFn: async (jobId) => await api.getStatus(jobId),
  });

  // 4. Handler functions
  const handleUpload = async () => {
    if (!fileUpload.file) {
      showToast('Please select a file', 'error');
      return;
    }
    await converter.handleUpload();
  };

  const handleDownload = async () => {
    // Download logic with toast feedback
  };

  const handleReset = () => {
    converter.handleReset();
    fileUpload.clearFile();
  };

  // 5. Sync file state
  React.useEffect(() => {
    converter.handleFileChange(fileUpload.file);
  }, [fileUpload.file]);

  // 6. Render with reusable components
  return (
    <div className="card">
      <FileUpload {...props} />
      {converter.error && <Alert type="error" message={converter.error} />}
      {!converter.status && <button onClick={handleUpload}>Upload</button>}
      {converter.status && <StatusDisplay {...props} />}
      <PipelineInfo steps={pipelineSteps} />
    </div>
  );
};
```

## Benefits of Refactoring

### Before
- **Tight coupling**: UI logic mixed with business logic
- **Code duplication**: Similar logic repeated in OMR and AMT converters
- **Hard to test**: useState hooks tightly coupled to components
- **Limited reusability**: Components weren't composable
- **No global state**: No way to show notifications across app

### After
- **Loose coupling**: Clear separation between UI, hooks, and services
- **DRY principle**: Shared logic in custom hooks
- **Testable**: Hooks and components can be tested independently
- **Highly reusable**: Components and hooks can be used anywhere
- **Global state management**: Toast context for app-wide notifications
- **Better UX**: Consistent error handling and user feedback

## Adding New Converters

To add a new converter (e.g., `PDFConverter`):

1. Create API methods in `services/api.ts`:
```typescript
uploadPDFFile: async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/api/pdf/upload', formData);
  return response.data;
},
```

2. Create converter component using the pattern:
```typescript
import { useFileConverter, useFileUpload } from '../hooks';
import { useToast } from '../contexts/ToastContext';
import { FileUpload, StatusDisplay, Alert, PipelineInfo } from './common';

const PDFConverter: React.FC = () => {
  const { showToast } = useToast();
  const fileUpload = useFileUpload({ accept: '.pdf' });
  const converter = useFileConverter({
    uploadFn: bandMusicAPI.uploadPDFFile,
    getStatusFn: bandMusicAPI.getJobStatus,
  });
  
  // Add handlers and render
};
```

3. Add to App.tsx:
```typescript
<div className="grid md:grid-cols-3 gap-8">
  <OMRConverter />
  <AMTConverter />
  <PDFConverter />
</div>
```

## File Organization

```
frontend/src/
├── components/
│   ├── common/              # Reusable UI components
│   │   ├── Alert.tsx
│   │   ├── FileUpload.tsx
│   │   ├── ProgressBar.tsx
│   │   ├── StatusDisplay.tsx
│   │   ├── PipelineInfo.tsx
│   │   ├── ToastContainer.tsx
│   │   └── index.ts         # Barrel export
│   ├── OMRConverter.tsx     # OMR feature component
│   └── AMTConverter.tsx     # AMT feature component
├── contexts/
│   └── ToastContext.tsx     # Global toast state
├── hooks/
│   ├── useFileConverter.ts  # File conversion logic
│   ├── useFileUpload.ts     # File upload logic
│   └── index.ts             # Barrel export
├── services/
│   └── api.ts               # API client
├── App.tsx                  # Root component
└── App.css                  # Global styles
```

## Testing Strategy

### Unit Tests
- Test custom hooks in isolation with `@testing-library/react-hooks`
- Test components with `@testing-library/react`
- Mock API calls with `jest.mock`

### Integration Tests
- Test complete converter workflows
- Test toast notifications appear correctly
- Test file validation logic

### Example Test
```typescript
import { renderHook } from '@testing-library/react-hooks';
import { useFileUpload } from './useFileUpload';

describe('useFileUpload', () => {
  it('validates file size', () => {
    const { result } = renderHook(() => 
      useFileUpload({ maxSize: 1024 })
    );
    
    const largefile = new File(['x'.repeat(2000)], 'large.pdf');
    result.current.setFile(largeFile);
    
    expect(result.current.error).toBeTruthy();
  });
});
```

## Performance Optimizations

1. **useCallback**: All event handlers wrapped in `useCallback`
2. **useEffect cleanup**: Polling stops on unmount
3. **Lazy component loading**: Could add `React.lazy()` for code splitting
4. **Memoization**: Could add `React.memo()` for expensive components

## Future Enhancements

1. **Error Boundaries**: Add React error boundaries for graceful error handling
2. **Loading States**: Add skeleton loaders for better perceived performance
3. **Drag & Drop**: Enhance FileUpload with drag-and-drop support
4. **Accessibility**: Add ARIA labels and keyboard navigation
5. **Animation**: Add transitions with Framer Motion or React Spring
6. **State Management**: Consider Zustand or Jotai for complex state
7. **Query Management**: Consider React Query for server state management
8. **Testing**: Add comprehensive test coverage with Jest and React Testing Library

## Migration Notes

The refactoring is **backward compatible** - the API contract remains the same. No backend changes required.

**Key Changes**:
- Replaced inline state management with custom hooks
- Added ToastProvider wrapper in App.tsx
- Replaced inline UI elements with reusable components
- Changed from tab-based to side-by-side layout

**No Breaking Changes**: All API endpoints and response formats remain unchanged.
