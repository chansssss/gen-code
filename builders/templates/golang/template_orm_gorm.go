package models

import "github.com/jinzhu/gorm"

type {{ name | singular_and_title }} struct {
	gorm.Model
	{% for column in columns -%}
    {% if column.name != 'id' and column.name != 'created_at' and column.name != 'updated_at' and column.name != 'deleted_at' -%}
    {{column.name|word2hump}}  {{column.type}} //
    {% endif -%}
    {% endfor -%}
}


func {{ name | singular_and_title }}GetByID({{ name | singular_and_flmbl }}ID uint) ({{ name | singular_and_flmbl }} *{{ name | singular_and_title }}, err error) {
	err = db.FirstOrInit(&{{ name | singular_and_flmbl }}, "id = ?", {{ name | singular_and_flmbl }}ID).Error
	return
}

func {{ name | singular_and_title }}New({{ name | singular_and_flmbl }} *{{ name | singular_and_title }}) error {
	return db.Create(&{{ name | singular_and_flmbl }}).Error
}

func {{ name | singular_and_title }}Update({{ name | singular_and_flmbl }} *{{ name | singular_and_title }}) error {
	return db.Save(&{{ name | singular_and_flmbl }}).Error
}

func {{ name | singular_and_title }}DeleteByID({{ name | singular_and_flmbl }}ID uint) error {
	return db.Delete(&{{ name | singular_and_title }}{}, "id = ?", {{ name | singular_and_flmbl }}ID).Error
}

func {{ name | singular_and_title }}List({{ name | singular_and_flmbl }}ID uint, page, limit int) (list []{{ name | singular_and_title }}, count int64, err error) {
	sql := db.Model(&{{ name | singular_and_title }}{})
	if {{ name | singular_and_flmbl }}ID > 0 {
		sql = sql.Where("id = ?", {{ name | singular_and_flmbl }}ID)
	}
	err = sql.Order("id desc").
		Offset(Offset(page, limit)).
		Limit(Limit(limit)).
		Find(&list).Error
	return
}
