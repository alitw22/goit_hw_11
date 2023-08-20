# please add annotation to the code:
# в данный код необходимо добавить аннотирование типов:

from collections import UserDict
from datetime import datetime, date
from typing import Optional, List, Union


class Field:
    def __init__(self, value: Union[str, int, date]):
        self.set_value(value)
    
    def get_value(self) -> Union[str, int, date]:
        return self._value
    
    def set_value(self, value: Union[str, int, date]):
        self._value = value

class Name(Field):
    pass

class Phone(Field):
    def set_value(self, value: str):
        if not self.validate_phone(value):
            raise ValueError("Invalid phone number")
        self._value = value
    
    def validate_phone(self, phone: str) -> bool:
        return True

class Birthday(Field):
    def set_value(self, value: date):
        if not self.validate_birthday(value):
            raise ValueError("Invalid birthday")
        self._value = value

    def validate_birthday(self, birthday: date) -> bool:
        return True

    def get_month(self) -> int:
        return self._value.month

    def get_day(self) -> int:
        return self._value.day

class Record:
    def __init__(self, name: str, phone: Optional[str] = None, birthday: Optional[date] = None):
        self.name = Name(name)
        self.phones: List[Phone] = []
        self.birthday = Birthday(birthday) if birthday else None

        if phone:
            self.add_phone(phone)
    
    def add_phone(self, phone: Union[str, Phone]):
        if isinstance(phone, str):
            self.phones.append(Phone(phone))
        elif isinstance(phone, Phone):
            self.phones.append(phone)
        else:
            raise ValueError("Invalid phone type")
    
    def remove_phone(self, phone: Union[str, Phone]):
        inx = self.get_index_by_phone(phone)
        if inx is None:
            raise ValueError(f"The phone not found {phone}") 
        del self.phones[inx]
        return f"The phone deleted {phone}"
    
    def get_index_by_phone(self, phone: Union[str, Phone]) -> Optional[int]:
        if isinstance(phone, Phone):
            phone = phone.get_value()
        for inx, _phone in enumerate(self.phones):
            if _phone.get_value() == phone:
                return inx
        return None

    def edit_phone(self, old_phone: Union[str, Phone], new_phone: str):
        for phone in self.phones:
            if phone.get_value() == old_phone:
                phone.set_value(new_phone)
                break
    
    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return None        

        today = datetime.now().date()        
        next_birthday = datetime(today.year, self.birthday.get_month(), self.birthday.get_day()).date()
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        days_remaining = (next_birthday - today).days
        return days_remaining

class AddressBook(UserDict):
    def __iter__(self):
        self._index = 0
        self._keys = list(self.data.keys())
        return self
    
    def __next__(self):
        if self._index < len(self._keys):
            record = self.data[self._keys[self._index]]
            self._index += 1
            return record
        raise StopIteration
    
    def iterator(self, page_size: int):
        self._index = 0
        self._keys = list(self.data.keys())
        while self._index < len(self._keys):
            yield self.data[self._keys[self._index]]
            self._index += 1
    
    def add_record(self, name: str, phones: Optional[List[str]] = None, birthday: Optional[date] = None):
        record = Record(name, birthday=birthday)
        if phones:
            for phone in phones:
                record.add_phone(phone)
        self.data[name] = record    
    
    def delete_record(self, name: str):
        del self.data[name]

    def edit_record(self, name: str, new_name: Optional[str] = None, new_phones: Optional[List[str]] = None):
        if name not in self.data:           
            return f"{name} Name not found "
        record = self.data[name]
        if new_name:
            record.name.set_value(new_name)

        if new_phones:
            record.phones = []
            for phone in new_phones:
                record.add_phone(phone)

    def find_records_by_name(self, name: str):
        results = []
        for record in self.data.values():
            if record.name.get_value() == name:
                results.append(record)
        return results

    def find_records_by_phone(self, phone: str):
        results = []
        for record in self.data.values():
            for record_phone in record.phones:
                if record_phone.get_value() == phone:
                    results.append(record)
                    break
        return results

if __name__ == "__main__":
    address_book = AddressBook()
