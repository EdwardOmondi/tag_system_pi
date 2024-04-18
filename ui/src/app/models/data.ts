export type Data = {
  scannerId: string;
  braceletId: string;
  timestamp: number;
};

export type Response = {
  Result: number;
  Message: string;
  data: ResponseData | null;
};

type ResponseData = {
  user: User;
  scanner: Scanner;
  bracelets: Bracelets;
};

type User = {
  id: string;
  name: string;
  email: string;
};

type Scanner = {
  id: string;
  name: string;
  points: string;
};

type Bracelets = {
  id: string;
  name: string;
  bracelet_type: string;
};
