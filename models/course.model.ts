import { Category } from './category.model';

export interface Course {
  id: number;
  title: string;
  description: string;
  category: Category;
}
