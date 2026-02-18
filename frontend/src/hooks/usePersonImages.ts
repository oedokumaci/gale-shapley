import { useState, useCallback } from 'react';

import type { PersonImages } from '@/types';

export function usePersonImages(initialImages: PersonImages = {}) {
  const [images, setImages] = useState<PersonImages>(initialImages);

  const uploadImage = useCallback((name: string, file: File) => {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result === 'string') {
        setImages((prev) => ({ ...prev, [name]: reader.result as string }));
      }
    };
    reader.readAsDataURL(file);
  }, []);

  const removeImage = useCallback((name: string) => {
    setImages((prev) => {
      const updated = { ...prev };
      delete updated[name];
      return updated;
    });
  }, []);

  return { images, uploadImage, removeImage };
}
